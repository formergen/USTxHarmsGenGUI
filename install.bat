@echo off
echo Checking for Python and pip...

where python
if %errorlevel% neq 0 (
    echo Python was not found in PATH. Please ensure Python is installed and added to your system's PATH environment variable.
    pause
    exit /b 1
)

where pip
if %errorlevel% neq 0 (
    echo pip was not found. Ensure pip is installed for your Python version.
    echo You might need to reinstall Python and select the "Add Python to PATH" option during installation.
    pause
    exit /b 1
)

echo Updating pip to the latest version...
python -m pip install --upgrade pip

echo Installing dependencies from requirements.txt...
python -m pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo All dependencies were installed successfully!
    pause
) else (
    echo An error occurred while installing dependencies.
    echo Please check the error output above and the requirements.txt file.
    pause
    exit /b 1
)