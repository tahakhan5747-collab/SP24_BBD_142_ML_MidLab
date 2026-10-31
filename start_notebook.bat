@echo off
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe goto missing
.venv\Scripts\python.exe -m notebook notebook\ML_Lab_Project.ipynb
if errorlevel 1 pause
exit /b
:missing
echo Double-click setup_windows.bat first.
pause
