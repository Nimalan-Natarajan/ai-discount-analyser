@echo off
echo 🚢 Starting AI-Driven Logistics Quotation Management Tool...
echo ============================================================

cd /d "C:\Users\ninatara\AIPredictiveDiscount\DiscountPredictor"

echo 🔧 Current directory: %cd%
echo 🌐 Starting Streamlit server...
echo ⚠️  Make sure your .env file contains your GEMINI_API_KEY
echo ============================================================

"C:\Users\ninatara\AIPredictiveDiscount\DiscountPredictor\venv\Scripts\python.exe" -m streamlit run src\app.py

pause
