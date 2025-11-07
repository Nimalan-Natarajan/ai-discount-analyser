#!/bin/bash
# Deployment preparation script for AI-Driven Discount Analyser

echo "🚀 Preparing AI-Driven Discount Analyser for deployment..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment (Windows)
if [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
elif [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
mkdir -p data/processed
mkdir -p logs

# Check for .env file
if [ ! -f ".env" ]; then
    echo "🔑 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your GEMINI_API_KEY"
fi

# Run tests
echo "🧪 Running tests..."
python -m pytest tests/ -v --tb=short

if [ $? -eq 0 ]; then
    echo "✅ All tests passed!"
    echo ""
    echo "🎉 Deployment preparation complete!"
    echo ""
    echo "📋 Next steps:"
    echo "1. Edit .env file and add your GEMINI_API_KEY"
    echo "2. Test locally: streamlit run src/app.py"
    echo "3. Push to GitHub for deployment"
    echo ""
    echo "🌐 Deployment options:"
    echo "- Streamlit Community Cloud (FREE): https://share.streamlit.io"
    echo "- Heroku: https://heroku.com"
    echo "- Railway: https://railway.app"
    echo ""
    echo "📖 See DEPLOYMENT_STEPS.md for detailed instructions"
else
    echo "❌ Tests failed. Please fix errors before deployment."
fi
