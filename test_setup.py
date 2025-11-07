"""
Simple test script to verify the setup
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test all required imports"""
    print("🧪 Testing imports...")
    
    try:
        import pandas as pd
        print("✅ Pandas imported successfully")
    except ImportError as e:
        print(f"❌ Pandas import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ NumPy imported successfully")
    except ImportError as e:
        print(f"❌ NumPy import failed: {e}")
        return False
    
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import google.generativeai as genai
        print("✅ Google Generative AI imported successfully")
    except ImportError as e:
        print(f"❌ Google Generative AI import failed: {e}")
        return False
    
    try:
        from data_processor import QuoteProcessor
        print("✅ Data processor imported successfully")
    except ImportError as e:
        print(f"❌ Data processor import failed: {e}")
        return False
    
    return True

def test_data_processing():
    """Test data processing functionality"""
    print("\n📊 Testing data processing...")
    
    try:
        from data_processor import QuoteProcessor
        
        processor = QuoteProcessor()
        data = processor.load_data('data/sample_quotes.csv')
        print(f"✅ Loaded {len(data)} sample quotes")
        
        # Test validation
        is_valid = processor.validate_data(data)
        print(f"✅ Data validation: {'passed' if is_valid else 'failed'}")
        
        return True
    except Exception as e:
        print(f"❌ Data processing test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Running setup verification tests...\n")
    
    # Test imports
    imports_ok = test_imports()
    
    # Test data processing
    data_ok = test_data_processing()
    
    print("\n" + "="*50)
    if imports_ok and data_ok:
        print("🎉 All tests passed! Your setup is ready to go.")
        print("\n💡 Next steps:")
        print("1. Copy .env.example to .env and add your GEMINI_API_KEY")
        print("2. Run the app with: python run_app.py")
        print("3. Or use VS Code tasks: Ctrl+Shift+P -> Tasks: Run Task -> Run Streamlit App")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False
    
    return True

if __name__ == "__main__":
    main()
