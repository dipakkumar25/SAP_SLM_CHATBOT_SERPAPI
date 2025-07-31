#!/bin/bash
echo "Starting SAP Smart Chatbot..."
cd "$(dirname "$0")"
if [ -f venv/bin/activate ]; then
    source venv/bin/activate
else
    echo "Virtual environment not found. Please run setup.sh first."
    exit 1
fi
streamlit run app.py