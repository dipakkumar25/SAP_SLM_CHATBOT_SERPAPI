#!/usr/bin/env python3
"""
Main Streamlit application file.
This should be run directly with: streamlit run app.py
"""

import sys
import os
import streamlit as st
import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Configuration
class Settings:
    SERPAPI_KEY = os.getenv("SERPAPI_KEY", "6bbf05bfc95ea39d257c1ed7076a78177c8b0deed5edbb6b38d5d66f056472a4")
    KB_DATA_PATH = os.getenv("KB_DATA_PATH", "kb_data/sap_kb.xlsx")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.7"))
    TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", "3"))
    APP_TITLE = "SAP Intelligent Support Assistant (SLM + RAG)"
    APP_DESCRIPTION = "Built with RAG-powered SAP SLM. For internal and external issue resolution."

settings = Settings()

# Utility functions
@st.cache_data
def load_kb(filepath):
    """Load knowledge base from Excel file."""
    try:
        df = pd.read_excel(filepath)
        df = df.dropna(subset=['Note Title', 'Description'])
        df['combined_text'] = df['Note Title'] + ". " + df['Description']
        return df
    except Exception as e:
        st.error(f"Error loading knowledge base: {str(e)}")
        return None

@st.cache_resource
def load_embedding_model():
    """Load the embedding model."""
    try:
        return SentenceTransformer(settings.EMBEDDING_MODEL)
    except Exception as e:
        st.error(f"Error loading embedding model: {str(e)}")
        return None

@st.cache_data
def get_kb_embeddings(kb_texts):
    """Get embeddings for knowledge base texts with caching."""
    model = load_embedding_model()
    if model is None:
        return None
    return model.encode(kb_texts)

@st.cache_resource
def build_search_index(_kb_embeddings):
    """Build FAISS index with caching."""
    dim = _kb_embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(_kb_embeddings)
    return index

def get_top_k(query, model, index, kb_texts, k=3, threshold=0.7):
    """Get top-k similar results."""
    query_vec = model.encode([query])
    D, I = index.search(np.array(query_vec), k)
    results = [(kb_texts[i], D[0][j]) for j, i in enumerate(I[0]) if D[0][j] < threshold]
    return results

def external_rag(query):
    """External search using SerpAPI."""
    if not settings.SERPAPI_KEY:
        return ["External search failed: API key not configured"]
    
    try:
        params = {
            "engine": "google",
            "q": query,
            "api_key": settings.SERPAPI_KEY,
            "num": 3
        }
        response = requests.get("https://serpapi.com/search", params=params)
        results = response.json().get("organic_results", [])
        return [f"{res['title']}: {res['link']}" for res in results]
    except Exception as e:
        return [f"External search failed: {str(e)}"]

# Main application
def main():
    st.set_page_config(
        page_title="SAP Support Assistant",
        page_icon="🔧",
        layout="wide"
    )
    
    st.title(settings.APP_TITLE)
    
    # Check if knowledge base exists
    if not os.path.exists(settings.KB_DATA_PATH):
        st.error(f"Knowledge base file not found: {settings.KB_DATA_PATH}")
        st.info("Please ensure your Excel file is placed in the kb_data/ folder with columns 'Note Title' and 'Description'")
        return
    
    # Load components
    kb = load_kb(settings.KB_DATA_PATH)
    if kb is None:
        st.error("Failed to load knowledge base. Please check your configuration.")
        return
    
    # Build search index with caching
    kb_texts = kb['combined_text'].tolist()
    
    # Use cached embeddings and index
    with st.spinner("Preparing search system... (this will be fast after first run)"):
        kb_embeddings = get_kb_embeddings(kb_texts)
        if kb_embeddings is None:
            st.error("Failed to generate embeddings.")
            return
        
        index = build_search_index(kb_embeddings)
        model = load_embedding_model()  # This is cached
        
        if model is None:
            st.error("Failed to load embedding model.")
            return
    
    # Search interface
    st.markdown("---")
    query = st.text_input("Enter your SAP infrastructure issue/question:", key="search_query")
    
    if query:
        with st.spinner("Searching..."):
            results = get_top_k(
                query, 
                model, 
                index, 
                kb_texts, 
                k=settings.TOP_K_RESULTS, 
                threshold=settings.SIMILARITY_THRESHOLD
            )
        
        if results:
            st.subheader("🔍 Internal Knowledge Base Results")
            for i, (text, score) in enumerate(results):
                confidence = round(1 - score, 2)
                with st.expander(f"Result {i+1} - Confidence: {confidence}", expanded=True):
                    st.markdown(text[:500] + "..." if len(text) > 500 else text)
        else:
            st.warning("No confident match found in internal KB. Redirecting to external sources...")
            st.subheader("🌐 External Suggested Links")
            
            with st.spinner("Searching external sources..."):
                external_results = external_rag(query)
            
            for link in external_results:
                st.markdown(f"• {link}")
    
    # Sidebar info
    with st.sidebar:
        st.markdown("### 📊 System Info")
        st.info(f"Knowledge Base: {len(kb)} entries")
        st.info(f"Model: {settings.EMBEDDING_MODEL}")
        st.info(f"Similarity Threshold: {settings.SIMILARITY_THRESHOLD}")
        
        st.markdown("### ⚙️ Configuration")
        api_status = "✅ Configured" if settings.SERPAPI_KEY else "❌ Not Configured"
        st.markdown(f"**API Key Status:** {api_status}")
        if settings.SERPAPI_KEY:
            st.markdown(f"**API Key:** {settings.SERPAPI_KEY[:8]}...")
        st.markdown(f"**KB File:** {settings.KB_DATA_PATH}")
        
        # Debug info
        st.markdown("### 🔧 Debug Info")
        st.text(f"Current working directory: {os.getcwd()}")
        st.text(f".env file exists: {os.path.exists('.env')}")
        if os.path.exists('.env'):
            with open('.env', 'r') as f:
                env_content = f.read()
                st.text(f"API key in .env: {'SERPAPI_KEY' in env_content}")
    
    st.markdown("---")
    st.caption(settings.APP_DESCRIPTION)

if __name__ == "__main__":
    main()