"""
Final launcher script for the AI Logistics Quotation Tool
This script ensures all paths are correct and launches the Streamlit app
"""
import subprocess
import sys
import os
from pathlib import Path
import time

def main():
    # Get the project directory
    project_dir = Path(__file__).parent.absolute()
    
    # Set up paths
    venv_python = project_dir / "venv" / "Scripts" / "python.exe"
    app_file = project_dir / "src" / "app.py"
    
    # Change to project directory
    os.chdir(project_dir)
    
    print("🚢 AI-Driven Logistics Quotation Management Tool")
    print("=" * 60)
    print(f"📁 Project Directory: {project_dir}")
    print(f"🐍 Python Executable: {venv_python}")
    print(f"📱 App File: {app_file}")
    print("=" * 60)
    
    # Check if files exist
    if not venv_python.exists():
        print("❌ Virtual environment Python not found!")
        print("Please ensure the virtual environment is set up correctly.")
        return False
    
    if not app_file.exists():
        print("❌ App file not found!")
        return False
    
    # Test data processing first
    print("🔧 Testing data processing...")
    try:
        # Add src to path for imports
        sys.path.insert(0, str(project_dir / "src"))
        
        from data_processor import QuoteProcessor
        processor = QuoteProcessor()
        
        # Test with sample data
        sample_file = project_dir / "data" / "sample_quotes.csv"
        if sample_file.exists():
            processed_data = processor.process_data(str(sample_file))
            print(f"✅ Data processing test successful: {len(processed_data)} records")
        else:
            print("⚠️  Sample data not found, but app should still work")
            
    except Exception as e:
        print(f"⚠️  Data processing test failed: {e}")
        print("🔄 The app will still launch, but you may need to check your data")

    # Test Gemini API
    print("\n🤖 Testing Gemini API...")
    try:
        from utils.config import Config
        if Config.GEMINI_API_KEY:
            from ai_predictor import DiscountPredictor
            predictor = DiscountPredictor()
            if predictor.model:
                print("✅ Gemini API configured and working")
            else:
                print("⚠️  Gemini API configured but model failed to load")
                print("💡 Run 'python fix_gemini.py' to diagnose and fix API issues")
        else:
            print("⚠️  No Gemini API key found - AI features will be disabled")
            print("💡 Add GEMINI_API_KEY to your .env file to enable AI predictions")
    except Exception as e:
        print(f"⚠️  Gemini API test failed: {e}")
        print("💡 You can still use all other features")

    # Launch the app
    try:
        print("\n🚀 Launching Streamlit app...")
        print("🌐 The app will be available at: http://localhost:8501")
        print("⚠️  Make sure your .env file contains a valid GEMINI_API_KEY")
        print("🛑 Press Ctrl+C to stop the server")
        print("=" * 60)
        
        # Run streamlit with simpler approach
        cmd = [str(venv_python), "-m", "streamlit", "run", str(app_file), 
               "--server.port=8501", "--server.headless=false"]
        
        # Launch and let it run
        subprocess.run(cmd, cwd=str(project_dir))
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        
    except Exception as e:
        print(f"❌ Error launching app: {e}")
        print("\n💡 Alternative launch methods:")
        print(f"1. Manual: {venv_python} -m streamlit run {app_file}")
        print(f"2. From VS Code: Use the 'Run Streamlit App' task")
        return False
    
    return True

if __name__ == "__main__":
    main()
