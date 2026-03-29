@echo off
echo =========================================
echo Voice Sales Agent - Local Server
echo =========================================
echo.
echo Starting FastAPI Server on port 8000...
echo.

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
pause
