#!/usr/bin/env python
"""
Simple test and launcher for the logistics quotation tool
"""

import os
import sys
from pathlib import Path

def setup_path():
    """Set up Python path for imports"""
    # Get the absolute path to this script's directory
    current_dir = Path(__file__).parent.absolute()
    src_dir = current_dir / "src"
    
    # Print debug info
    print(f"🔧 Current directory: {current_dir}")
    print(f"🔧 Source directory: {src_dir}")
    
    # Add src to path if not already there
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))
    
    # Change to project directory
    os.chdir(current_dir)
    
    return src_dir

def test_imports():
    """Test all required imports"""
    print("🧪 Testing imports...")
    
    try:
        import pandas as pd
        print("✅ pandas: OK")
    except ImportError as e:
        print(f"❌ pandas: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ numpy: OK")
    except ImportError as e:
        print(f"❌ numpy: {e}")
        return False
    
    try:
        import streamlit as st
        print("✅ streamlit: OK")
    except ImportError as e:
        print(f"❌ streamlit: {e}")
        return False
    
    try:
        from data_processor import QuoteProcessor
        print("✅ data_processor: OK")
    except ImportError as e:
        print(f"❌ data_processor: {e}")
        return False
    
    try:
        from ai_predictor import DiscountPredictor
        print("✅ ai_predictor: OK")
    except ImportError as e:
        print(f"❌ ai_predictor: {e}")
        return False
    
    try:
        from static_analyzer import StaticAnalyzer
        print("✅ static_analyzer: OK")
    except ImportError as e:
        print(f"❌ static_analyzer: {e}")
        return False
    
    return True

def test_data_loading():
    """Test data loading"""
    print("\n📊 Testing data loading...")
    
    try:
        from data_processor import QuoteProcessor
        processor = QuoteProcessor()
        
        # Check if sample data exists
        data_file = Path("data/sample_quotes.csv")
        if not data_file.exists():
            print(f"❌ Sample data file not found: {data_file}")
            return False
        
        # Try to load data
        data = processor.load_data(str(data_file))
        print(f"✅ Loaded {len(data)} sample quotes")
        
        return True
    except Exception as e:
        print(f"❌ Data loading failed: {e}")
        return False

def launch_app():
    """Launch the Streamlit app"""
    print("\n🚀 Launching application...")
    
    try:
        import subprocess
        
        # Use the virtual environment's python
        venv_python = Path("venv/Scripts/python.exe")
        if not venv_python.exists():
            print("❌ Virtual environment not found. Using system python.")
            python_cmd = "python"
        else:
            python_cmd = str(venv_python)
        
        app_file = Path("src/app.py")
        
        cmd = [python_cmd, "-m", "streamlit", "run", str(app_file)]
        
        print(f"Running: {' '.join(cmd)}")
        print("🌐 The app should open in your browser at http://localhost:8501")
        print("=" * 60)
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
    except Exception as e:
        print(f"❌ Failed to launch app: {e}")
        return False
    
    return True

def main():
    """Main function"""
    print("🚢 AI-Driven Logistics Quotation Management Tool")
    print("=" * 60)
    
    # Setup path
    src_dir = setup_path()
    
    # Run tests
    imports_ok = test_imports()
    if not imports_ok:
        print("\n❌ Import tests failed. Please check your Python environment.")
        return False
    
    data_ok = test_data_loading()
    if not data_ok:
        print("\n❌ Data loading test failed.")
        return False
    
    print("\n✅ All tests passed!")
    
    # Ask user if they want to launch the app
    response = input("\n🚀 Launch the application? (y/N): ").strip().lower()
    if response in ['y', 'yes']:
        launch_app()
    else:
        print("👍 You can launch manually with: python launch_app.py")
        print("Or use: streamlit run src/app.py")

if __name__ == "__main__":
    main()
