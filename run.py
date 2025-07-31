#!/usr/bin/env python3
"""
Entry point for the SAP Smart Chatbot application.
Run this file to start the Streamlit app.
"""

import sys
import os
import subprocess

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def run_streamlit():
    """Run the Streamlit app using subprocess."""
    try:
        # Try to run streamlit directly
        subprocess.run([sys.executable, "-m", "streamlit", "run", __file__], check=True)
    except subprocess.CalledProcessError:
        print("Error: Streamlit not found. Please install it first:")
        print("pip install streamlit")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: Python not found in PATH")
        sys.exit(1)

if __name__ == "__main__":
    # If run directly, start streamlit
    if len(sys.argv) == 1:
        run_streamlit()
    else:
        # This is when called by streamlit
        from src.main import main
        main()