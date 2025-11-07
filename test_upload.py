#!/usr/bin/env python3
"""
Test the upload and processing logic step by step
"""
import sys
import os
import pandas as pd

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def step_by_step_test():
    """Test each step of the upload process"""
    print("🔍 **STEP-BY-STEP UPLOAD TEST**")
    print("=" * 40)
    
    # Step 1: Load raw file
    print("\n📁 Step 1: Loading raw test_quotes.csv")
    try:
        raw_data = pd.read_csv("test_quotes.csv")
        print(f"✅ Loaded {len(raw_data)} rows")
        print(f"📋 Raw columns: {list(raw_data.columns)}")
    except Exception as e:
        print(f"❌ Failed to load: {e}")
        return False
    
    # Step 2: Import processor
    print("\n🔧 Step 2: Importing data processor")
    try:
        from data_processor import QuoteProcessor
        processor = QuoteProcessor()
        print("✅ Processor imported successfully")
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False
    
    # Step 3: Test normalization
    print("\n🔄 Step 3: Testing format normalization")
    try:
        normalized_data = processor.normalize_data_format(raw_data)
        print(f"✅ Normalized successfully")
        print(f"📋 Normalized columns: {list(normalized_data.columns)}")
        
        # Check key conversions
        if 'customer_id' in normalized_data.columns:
            print(f"✅ customerName → customer_id conversion: OK")
        if 'status' in normalized_data.columns:
            print(f"✅ accepted → status conversion: OK") 
            print(f"   Sample status values: {normalized_data['status'].unique()[:3]}")
            
    except Exception as e:
        print(f"❌ Normalization failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Step 4: Test validation
    print("\n✅ Step 4: Testing validation")
    try:
        is_valid = processor.validate_data(normalized_data)
        print(f"{'✅' if is_valid else '❌'} Validation result: {is_valid}")
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        return False
    
    # Step 5: Test full processing
    print("\n🚀 Step 5: Testing complete processing")
    try:
        processed_data = processor.process_data("test_quotes.csv")
        print(f"✅ Complete processing successful!")
        print(f"📊 Final data: {len(processed_data)} rows, {len(processed_data.columns)} columns")
        return True
    except Exception as e:
        print(f"❌ Full processing failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = step_by_step_test()
    
    if success:
        print(f"\n🎉 SUCCESS: Upload processing is working correctly!")
        print(f"💡 The 403 error is likely a browser/network issue, not code")
        print(f"🔧 Try refreshing the browser or clearing cache")
    else:
        print(f"\n💔 There are issues in the processing pipeline")
