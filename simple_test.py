import pandas as pd
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Test basic import
try:
    from data_processor import QuoteProcessor
    print("Import successful!")
    
    # Test with test_quotes.csv
    if os.path.exists("test_quotes.csv"):
        print("test_quotes.csv found!")
        df = pd.read_csv("test_quotes.csv")
        print(f"Columns: {list(df.columns)}")
        print(f"Shape: {df.shape}")
    else:
        print("test_quotes.csv not found!")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
