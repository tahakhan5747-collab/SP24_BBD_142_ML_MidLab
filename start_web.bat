@echo off
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe goto missing
echo Open http://127.0.0.1:8000 after the server starts.
echo Keep this window open while using the website.
.venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
pause
exit /b
:missing
echo Double-click setup_windows.bat first.
pause
