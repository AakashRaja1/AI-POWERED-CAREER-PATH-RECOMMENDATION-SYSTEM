@echo off
REM GPU Training Launcher - Checks for PyTorch CUDA and starts training
setlocal enabledelayedexpansion

echo Activating Python environment...
call venv\Scripts\activate.bat

:CHECK_GPU
cls
echo [GPU Training Launcher]
echo.
echo Checking GPU PyTorch installation...
python -c "import torch; print('GPU CUDA Available:',torch.cuda.is_available()); cuda_ver=torch.version.cuda; print('CUDA Version:',cuda_ver if cuda_ver else 'N/A')" >nul 2>&1
if errorlevel 1 (
    echo ✗ GPU PyTorch still installing...
    echo Please wait 2-3 minutes and run this script again.
    echo.
    pause
    goto CHECK_GPU
)

echo ✓ GPU PyTorch ready!
echo.
echo Starting CNN training on GPU...
echo This will train the personality recognition model for best results.
echo.
python backend\ml_personality_pipeline\gpu_train_optimal.py

pause
