@echo off
echo =========================================
echo Voice Sales Agent - Initial Setup
echo =========================================

echo.
echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Initializing Database with Hardware Items...
python init_db.py

echo.
echo Setup Complete! 
echo You can now use run_with_ngrok.bat to start the server.
echo.
pause
