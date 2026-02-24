@echo off
echo ================================================================================
echo                     AD LAB DAY 7 - INSTALLATION
echo ================================================================================
echo.

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo.
echo Installing required packages...
echo This may take several minutes...
echo.

python -m pip install --upgrade pip
python -m pip install tensorflow>=2.13.0
python -m pip install numpy>=1.24.3
python -m pip install matplotlib>=3.7.1
python -m pip install scikit-learn>=1.3.0
python -m pip install seaborn>=0.12.2
python -m pip install pandas>=2.0.3

echo.
echo ================================================================================
echo Installation complete!
echo ================================================================================
echo.
echo Next steps:
echo   1. Run all questions:        python run_all.py
echo   2. Run individual questions: python q1.py
echo.
pause
