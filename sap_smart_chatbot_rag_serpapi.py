import streamlit as st
import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import requests

# Load the knowledge base from Excel
def load_kb(filepath='kb_data/sap_kb.xlsx'):
    df = pd.read_excel(filepath)
    df = df.dropna(subset=['Note Title', 'Description'])
    df['combined_text'] = df['Note Title'] + ". " + df['Description']
    return df

# Build embedding model
def load_embedding_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

# Build FAISS index
def build_faiss_index(embeddings):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index

# Perform search
def get_top_k(query, model, index, kb_texts, k=3, threshold=0.7):
    query_vec = model.encode([query])
    D, I = index.search(np.array(query_vec), k)
    results = [(kb_texts[i], D[0][j]) for j, i in enumerate(I[0]) if D[0][j] < threshold]
    return results

# External fallback RAG using SerpAPI
def external_rag(query):
    try:
        serp_api_key = "<YOUR_SERPAPI_KEY>"  # Replace with your SerpAPI key
        params = {
            "engine": "google",
            "q": query,
            "api_key": serp_api_key,
            "num": 3
        }
        response = requests.get("https://serpapi.com/search", params=params)
        results = response.json().get("organic_results", [])
        return [f"{res['title']}: {res['link']}" for res in results]
    except Exception as e:
        return [f"External search failed: {str(e)}"]

# UI
st.title("SAP Intelligent Support Assistant (SLM + RAG)")

query = st.text_input("Enter your SAP infrastructure issue/question:")

if query:
    with st.spinner("Thinking..."):
        kb = load_kb()
        model = load_embedding_model()
        kb_texts = kb['combined_text'].tolist()
        kb_embeddings = model.encode(kb_texts)
        index = build_faiss_index(np.array(kb_embeddings))
        results = get_top_k(query, model, index, kb_texts)

    if results:
        st.subheader("Internal Knowledge Base Results")
        for res, score in results:
            st.markdown(f"**Confidence:** {round(1 - score, 2)}\n\n{res[:300]}...")
    else:
        st.warning("No confident match found in internal KB. Redirecting to external sources...")
        st.subheader("External Suggested Links")
        external_results = external_rag(query)
        for link in external_results:
            st.write(link)

st.markdown("---")
st.caption("Built with RAG-powered SAP SLM. For internal and external issue resolution.")
