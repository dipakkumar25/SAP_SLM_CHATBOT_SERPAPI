# SAP Smart Chatbot RAG

An intelligent support assistant for SAP infrastructure issues using Retrieval-Augmented Generation (RAG) with FAISS indexing and SerpAPI fallback.

## Features

- **Internal Knowledge Base**: FAISS-powered similarity search
- **External Search**: SerpAPI integration for broader coverage
- **Streamlit UI**: User-friendly web interface
- **Modular Architecture**: Clean, maintainable code structure

## Quick Start

### Windows:
1. Run `setup.bat` (one-time setup)
2. Run `start.bat` to launch the app

### Linux/Mac:
1. Run `chmod +x setup.sh start.sh`
2. Run `./setup.sh` (one-time setup)
3. Run `./start.sh` to launch the app

### Manual Setup:

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate