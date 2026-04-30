@echo off
REM CPU Training Launcher with Live Progress
REM Installs tqdm if needed and starts training with real-time monitoring

setlocal enabledelayedexpansion

echo.
echo ================================================================================
echo                    GPU CPU PERSONALITY CNN TRAINING
echo ================================================================================
echo.

echo Activating Python environment...
call venv\Scripts\activate.bat

echo.
echo Installing required dependencies...
python -m pip install tqdm -q

echo.
echo ================================================================================
echo                         STARTING CPU TRAINING
echo ================================================================================
echo.
echo This will display LIVE PROGRESS with real-time metrics for each batch and epoch.
echo.

python backend\ml_personality_pipeline\train_cpu.py

echo.
pause
