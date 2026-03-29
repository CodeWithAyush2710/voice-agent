@echo off
echo ==============================================================
echo Voice Sales Agent - Server + Public URL (Ngrok)
echo ==============================================================
echo.

:: Start Local server in a new command window
echo Starting FastAPI Server...
start cmd /k "title Voice Agent API && uvicorn main:app --host 0.0.0.0 --port 8000"

:: Wait 3 seconds for it to boot
timeout /t 3 /nobreak >nul

:: Start Ngrok in the current window
echo.
echo Starting Ngrok on port 8000...
echo (Look for the "Forwarding" HTTPS URL and copy it to your Vapi webhook settings)
echo.
ngrok http 8000

pause
