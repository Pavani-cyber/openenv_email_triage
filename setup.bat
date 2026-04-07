@echo off
REM Quick setup script for Email Triage OpenEnv (Windows)
REM Run: setup.bat

setlocal enabledelayedexpansion

echo.
echo  Setting up Email Triage OpenEnv...
echo.

REM 1. Create virtual environment
echo [1/4] Creating virtual environment...
if not exist venv (
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)

REM 2. Activate venv
echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated

REM 3. Install dependencies
echo [3/4] Installing dependencies...
python -m pip install --upgrade pip setuptools wheel
if errorlevel 1 (
    echo WARNING: pip upgrade had issues, continuing anyway...
)

REM Install numpy first with pre-built wheels
echo Installing numpy 1.24.3 (model-compatible version^)...
python -m pip install --only-binary :all: numpy==1.24.3
if errorlevel 1 (
    echo WARNING: numpy install had issues, continuing...
)

REM Install remaining dependencies
python -m pip install --no-build-isolation --no-cache-dir -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    echo Try upgrading pip manually:
    echo   python -m pip install --upgrade pip setuptools wheel
    echo   python -m pip install --only-binary :all: numpy==1.24.3
    echo   python -m pip install -r requirements.txt
    pause
    exit /b 1
)
echo ✓ Dependencies installed

REM 4. Check for pre-trained model
echo [4/4] Checking for pre-trained model...
if not exist ppo_email_triage.zip (
    echo.
    echo Training new model (this may take 5-10 minutes^)...
    python train.py
    if errorlevel 1 (
        echo WARNING: Training may not have completed, but setup is done
    )
) else (
    echo ✓ Pre-trained model found
)

echo.
echo  Setup complete!
echo.
echo Next steps:
echo   1. Activate environment: venv\Scripts\activate.bat
echo   2. Run Gradio demo: python app_gradio.py
echo   3. Or run FastAPI: uvicorn app.main:app --reload
echo.
echo Docker deployment:
echo   docker build -t email-triage:latest .
echo   docker run -p 7860:7860 email-triage:latest
echo.
pause