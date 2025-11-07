#!/usr/bin/env python3
"""
Quick test script to verify format conversion works correctly
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import pandas as pd
from data_processor import QuoteProcessor

def test_format_conversion():
    """Test the format conversion from test_quotes.csv"""
    print("Testing format conversion...")
    
    processor = QuoteProcessor()
    
    # Test with test_quotes.csv if it exists
    if os.path.exists("test_quotes.csv"):
        print("\nTesting with test_quotes.csv:")
        
        # Load raw data
        raw_data = pd.read_csv("test_quotes.csv")
        print(f"Raw data columns: {list(raw_data.columns)}")
        print(f"Raw data shape: {raw_data.shape}")
        print(f"Sample accepted values: {raw_data['accepted'].unique()}")
        
        # Test normalization
        normalized_data = processor.normalize_data_format(raw_data)
        print(f"Normalized columns: {list(normalized_data.columns)}")
        print(f"Normalized shape: {normalized_data.shape}")
        print(f"Sample status values: {normalized_data['status'].unique()}")
        
        # Test validation
        is_valid = processor.validate_data(normalized_data)
        print(f"Data validation result: {is_valid}")
        
        # Show sample of first few rows
        print("\nFirst 3 rows of normalized data:")
        print(normalized_data.head(3).to_string())
        
    else:
        print("test_quotes.csv not found in current directory")
        return False
    
    return True

if __name__ == "__main__":
    test_format_conversion()
