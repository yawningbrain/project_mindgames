@echo off
REM Setup script for emotiv-lsl environment on Windows

echo ==========================================
echo Emotiv LSL Environment Setup
echo ==========================================
echo.

REM Check Python version
echo Checking Python version...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

python --version
echo.

REM Check if virtual environment exists
if exist "venv" (
    echo Virtual environment already exists
) else (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1
echo pip upgraded
echo.

REM Install package
echo Installing emotiv-lsl...
pip install -e . >nul 2>&1
echo emotiv-lsl installed
echo.

REM Ask about development dependencies
set /p install_dev="Install development dependencies? (y/N) "
if /i "%install_dev%"=="y" (
    echo Installing development dependencies...
    pip install -e ".[dev]" >nul 2>&1
    echo Development dependencies installed
)
echo.

REM Create .env from example if it doesn't exist
if not exist ".env" (
    if exist ".env.example" (
        echo Creating .env file from .env.example...
        copy .env.example .env >nul
        echo .env file created
        echo Please review and edit .env file if needed
    )
)
echo.

echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo Next steps:
echo 1. Activate the virtual environment:
echo    venv\Scripts\activate
echo.
echo 2. Configure settings in .env or config.py
echo.
echo 3. Connect your Emotiv EPOC X headset
echo.
echo 4. Run the LSL server:
echo    python main.py
echo.
echo For more information, see README.md
echo.
pause

