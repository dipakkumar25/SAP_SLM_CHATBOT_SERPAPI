@echo off
echo Starting SAP Smart Chatbot...
cd /d "%~dp0"
if exist venv\Scripts\activate (
    call venv\Scripts\activate
) else (
    echo Virtual environment not found. Please run setup.bat first.
    pause
    exit /b 1
)
streamlit run app.py
pause