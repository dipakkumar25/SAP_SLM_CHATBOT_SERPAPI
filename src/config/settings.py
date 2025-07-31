import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # API Keys
    SERPAPI_KEY = os.getenv("SERPAPI_KEY", "6bbf05bfc95ea39d257c1ed7076a78177c8b0deed5edbb6b38d5d66f056472a4")
    
    # File paths
    KB_DATA_PATH = os.getenv("KB_DATA_PATH", "kb_data/sap_kb.xlsx")
    
    # Model settings
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.7"))
    TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", "3"))
    
    # UI settings
    APP_TITLE = "SAP Intelligent Support Assistant (SLM + RAG)"
    APP_DESCRIPTION = "Built with RAG-powered SAP SLM. For internal and external issue resolution."

settings = Settings()