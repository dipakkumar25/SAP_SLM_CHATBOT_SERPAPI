@echo off
echo Setting up SAP Smart Chatbot...
cd /d "%~dp0"
python -m venv venv
call venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
echo.
echo Setup complete! You can now run start.bat
pause