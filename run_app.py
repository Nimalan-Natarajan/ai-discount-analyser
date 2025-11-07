"""
Launcher script for the AI-Driven Logistics Quotation Management Tool
"""
import subprocess
import sys
import os
from pathlib import Path

def main():
    """Launch the Streamlit application"""
    print("🚢 Starting AI-Driven Logistics Quotation Management Tool...")
    print("=" * 60)
    
    # Get the project root directory
    project_root = Path(__file__).parent
    
    # Set environment
    os.chdir(project_root)
    
    # Check if virtual environment exists
    venv_python = project_root / "venv" / "Scripts" / "python.exe"
    
    if not venv_python.exists():
        print("❌ Virtual environment not found!")
        print("Please run: python -m venv venv")
        print("Then activate it and install dependencies: pip install -r requirements.txt")
        sys.exit(1)
    
    # Launch Streamlit app
    app_path = project_root / "src" / "app.py"
    
    try:
        print(f"🌐 Launching Streamlit app from: {app_path}")
        print("📝 The app will open in your default web browser")
        print("⚠️  Don't forget to set your GEMINI_API_KEY in .env file for AI features")
        print("=" * 60)
        
        subprocess.run([
            str(venv_python),
            "-m", "streamlit", "run", str(app_path)
        ], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching app: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
        sys.exit(0)

if __name__ == "__main__":
    main()
