#!/bin/bash
echo "Setting up SAP Smart Chatbot..."
cd "$(dirname "$0")"
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
echo
echo "Setup complete! You can now run ./start.sh"