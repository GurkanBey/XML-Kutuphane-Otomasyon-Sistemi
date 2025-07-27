@echo off
REM Setup script for XML Library System
REM This will create a virtual environment and install required packages

echo === Setting up XML Library System ===

REM Create virtual environment
echo Creating virtual environment...
cd backend
python -m venv venv
if %errorlevel% neq 0 (
    echo Failed to create virtual environment.
    echo Make sure Python is installed and in your PATH.
    exit /b %errorlevel%
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
if %errorlevel% neq 0 (
    echo Failed to activate virtual environment.
    exit /b %errorlevel%
)

REM Install required packages
echo Installing required packages...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install required packages.
    exit /b %errorlevel%
)

echo === Setup Complete ===
echo.
echo To run the application:
echo 1. Activate the virtual environment: 
echo    cd backend
echo    venv\Scripts\activate
echo.
echo 2. Run the Flask application:
echo    python run.py
echo.
echo 3. Open the frontend in a browser:
echo    Simply open frontend/index.html in your browser
echo.
echo Test the API functionality:
echo    python tests\api_test.py --test all
echo.
echo Sample users:
echo   - Admin: username=admin, password=admin123
echo   - Student: username=student, password=student123
echo.
echo For complete documentation, see:
echo   - README.md: Main documentation
echo   - API_DOCUMENTATION.md: API endpoints reference
echo   - TESTING_GUIDE.md: Comprehensive testing guide
echo   - HOW_TO_USE_XML_TRANSFORMATION.md: XML transformation guide
echo   - XML_PARSING_TECHNIQUES.md: XML parsing methods
echo.
echo Press any key to exit...
pause > nul
