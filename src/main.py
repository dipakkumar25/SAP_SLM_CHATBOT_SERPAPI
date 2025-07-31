import streamlit as st
import numpy as np
from .config.settings import settings
from .utils.data_loader import load_kb
from .models.embedding_model import EmbeddingModel
from .models.search_engine import SearchEngine
from .utils.external_search import ExternalSearcher

def main():
    st.title(settings.APP_TITLE)
    
    # Initialize components
    @st.cache_resource
    def load_components():
        kb = load_kb(settings.KB_DATA_PATH)
        embedding_model = EmbeddingModel(settings.EMBEDDING_MODEL)
        search_engine = SearchEngine(embedding_model)
        search_engine.build_index(kb['combined_text'].tolist())
        external_searcher = ExternalSearcher()
        return kb, search_engine, external_searcher
    
    try:
        kb, search_engine, external_searcher = load_components()
        
        query = st.text_input("Enter your SAP infrastructure issue/question:")
        
        if query:
            with st.spinner("Thinking..."):
                results = search_engine.search(
                    query, 
                    k=settings.TOP_K_RESULTS, 
                    threshold=settings.SIMILARITY_THRESHOLD
                )
            
            if results:
                st.subheader("Internal Knowledge Base Results")
                for text, score in results:
                    confidence = round(1 - score, 2)
                    st.markdown(f"**Confidence:** {confidence}\n\n{text[:300]}...")
            else:
                st.warning("No confident match found in internal KB. Redirecting to external sources...")
                st.subheader("External Suggested Links")
                external_results = external_searcher.search(query)
                for link in external_results:
                    st.write(link)
        
        st.markdown("---")
        st.caption(settings.APP_DESCRIPTION)
        
    except Exception as e:
        st.error(f"Error loading application: {str(e)}")
        st.info("Please check your configuration and data files.")

if __name__ == "__main__":
    main()