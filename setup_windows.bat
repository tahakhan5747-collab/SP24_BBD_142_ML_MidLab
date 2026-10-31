@echo off
cd /d "%~dp0"
echo Setting up the ML Lab for 64-bit Python 3.11, 3.12, 3.13 or 3.14.
echo Internet is required for package downloads.
if exist .venv\Scripts\python.exe goto check_environment

for %%V in (3.14 3.13 3.12 3.11) do (
    py -%%V -c "import struct,sys; sys.exit(0 if struct.calcsize('P') == 8 else 1)" >nul 2>&1
    if not errorlevel 1 (
        py -%%V -m venv .venv
        if errorlevel 1 goto fail
        goto check_environment
    )
)
python -c "import sys,struct; sys.exit(0 if sys.version_info[:2] in [(3,11),(3,12),(3,13),(3,14)] and struct.calcsize('P') == 8 else 1)" >nul 2>&1
if errorlevel 1 goto need_python
python -m venv .venv
if errorlevel 1 goto fail

:check_environment
.venv\Scripts\python.exe -c "import sys,struct; print('Using Python',sys.version.split()[0],str(struct.calcsize('P')*8)+'-bit'); sys.exit(0 if sys.version_info[:2] in [(3,11),(3,12),(3,13),(3,14)] and struct.calcsize('P') == 8 else 1)"
if errorlevel 1 goto incompatible_environment
.venv\Scripts\python.exe -m pip install --upgrade pip
if errorlevel 1 goto fail
.venv\Scripts\python.exe -m pip install --only-binary=:all: -r requirements-notebook.txt
if errorlevel 1 goto fail
echo.
echo Setup complete. Double-click start_notebook.bat to open Jupyter.
echo For the small website, double-click start_web.bat.
pause
exit /b 0

:incompatible_environment
echo.
echo Existing .venv uses an unsupported Python version or architecture.
echo Rename .venv to .venv_old, then rerun setup with 64-bit Python 3.11-3.14 installed.
pause
exit /b 1

:need_python
echo Install a regular 64-bit Python 3.11, 3.12, 3.13 or 3.14, then rerun setup.
pause
exit /b 1

:fail
echo Setup did not complete. Read the error above; do not install build tools blindly.
echo This setup requests prebuilt packages and will not compile pandas locally.
pause
exit /b 1
