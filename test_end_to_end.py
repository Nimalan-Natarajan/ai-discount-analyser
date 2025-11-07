#!/usr/bin/env python3
"""
End-to-end test for the format conversion
"""
import sys
import os
import pandas as pd

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_end_to_end():
    print("🧪 Testing End-to-End Format Conversion...")
    
    try:
        from data_processor import QuoteProcessor
        
        processor = QuoteProcessor()
        
        # Test 1: Load test_quotes.csv (the new format)
        print("\n📊 Test 1: Loading test_quotes.csv")
        if os.path.exists("test_quotes.csv"):
            data = processor.load_data("test_quotes.csv")
            print(f"✅ Successfully loaded {len(data)} records")
            print(f"   Columns: {list(data.columns)}")
            print(f"   Status values: {data['status'].unique()}")
            
            # Test validation
            is_valid = processor.validate_data(data)
            print(f"   Validation: {'✅ PASSED' if is_valid else '❌ FAILED'}")
            
            # Show first row
            print(f"   Sample row: {data.iloc[0].to_dict()}")
            
        else:
            print("❌ test_quotes.csv not found")
            return False
        
        # Test 2: Test with sample data (old format)
        print("\n📊 Test 2: Testing with sample data")
        if os.path.exists("data/sample_quotes.csv"):
            old_data = processor.load_data("data/sample_quotes.csv")
            print(f"✅ Successfully loaded {len(old_data)} records from sample data")
            print(f"   Columns: {list(old_data.columns)}")
            
            is_valid_old = processor.validate_data(old_data)
            print(f"   Validation: {'✅ PASSED' if is_valid_old else '❌ FAILED'}")
        else:
            print("⚠️ data/sample_quotes.csv not found (optional)")
        
        print("\n🎉 All tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_end_to_end()
    exit(0 if success else 1)
