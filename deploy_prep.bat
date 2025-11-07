@echo off
REM Deployment preparation script for Windows
echo 🚀 Preparing AI-Driven Discount Analyser for deployment...

REM Check if virtual environment exists
if not exist "venv\" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo 📚 Installing dependencies...
pip install -r requirements.txt

REM Create necessary directories
if not exist "data\processed\" mkdir data\processed
if not exist "logs\" mkdir logs

REM Check for .env file
if not exist ".env" (
    echo 🔑 Creating .env file from template...
    copy .env.example .env
    echo ⚠️  Please edit .env and add your GEMINI_API_KEY
)

REM Run tests
echo 🧪 Running tests...
python -m pytest tests\ -v --tb=short

if %errorlevel% == 0 (
    echo ✅ All tests passed!
    echo.
    echo 🎉 Deployment preparation complete!
    echo.
    echo 📋 Next steps:
    echo 1. Edit .env file and add your GEMINI_API_KEY
    echo 2. Test locally: streamlit run src/app.py
    echo 3. Push to GitHub for deployment
    echo.
    echo 🌐 Deployment options:
    echo - Streamlit Community Cloud (FREE^): https://share.streamlit.io
    echo - Heroku: https://heroku.com
    echo - Railway: https://railway.app
    echo.
    echo 📖 See DEPLOYMENT_STEPS.md for detailed instructions
) else (
    echo ❌ Tests failed. Please fix errors before deployment.
)

pause
