"""
Fixed startup script for the Streamlit app
"""
import os
import sys
from pathlib import Path

# Add the src directory to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

# Change to project root directory
os.chdir(current_dir)

# Now import and run the app
if __name__ == "__main__":
    import streamlit.cli as stcli
    import sys
    
    # Set up the streamlit command
    sys.argv = ["streamlit", "run", str(src_dir / "app.py"), "--server.port=8501", "--server.headless=false"]
    
    print("🚢 Starting AI-Driven Logistics Quotation Management Tool...")
    print("🌐 Opening in your browser at: http://localhost:8501")
    print("⚠️  Make sure your .env file contains your GEMINI_API_KEY")
    print("=" * 60)
    
    # Run streamlit
    stcli.main()
