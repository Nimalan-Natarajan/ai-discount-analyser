"""
Debug script to identify the data validation issue
"""
import sys
import os
sys.path.append('src')

def debug_data_processing():
    print("🔧 Debugging Data Processing...")
    
    try:
        # Test basic imports
        import pandas as pd
        print("✅ Pandas import: OK")
        
        # Test loading CSV
        data_file = 'data/sample_quotes.csv'
        if not os.path.exists(data_file):
            print(f"❌ Data file not found: {data_file}")
            return False
        
        df = pd.read_csv(data_file)
        print(f"✅ Data loaded: {len(df)} rows, {len(df.columns)} columns")
        print(f"📋 Columns: {list(df.columns)}")
        
        # Check for missing values
        missing = df.isnull().sum()
        if missing.any():
            print("⚠️ Missing values found:")
            for col, count in missing[missing > 0].items():
                print(f"  - {col}: {count} missing")
        else:
            print("✅ No missing values")
        
        # Test data processor import
        from data_processor import QuoteProcessor
        print("✅ QuoteProcessor import: OK")
        
        # Test processor initialization
        processor = QuoteProcessor()
        print("✅ Processor initialization: OK")
        
        # Test data loading
        loaded_data = processor.load_data(data_file)
        print(f"✅ Processor load_data: {len(loaded_data)} rows")
        
        # Test validation step by step
        print("\n🔍 Testing validation steps...")
        
        # Check required columns
        required_columns = [
            'customer_id', 'date', 'shipment_type', 'commodity_type',
            'shipper_country', 'shipper_station', 'consignee_country',
            'consignee_station', 'discount_offered', 'status'
        ]
        
        missing_columns = [col for col in required_columns if col not in loaded_data.columns]
        if missing_columns:
            print(f"❌ Missing columns: {missing_columns}")
        else:
            print("✅ All required columns present")
        
        # Check data types
        print(f"\n📊 Data types:")
        for col in required_columns:
            if col in loaded_data.columns:
                print(f"  - {col}: {loaded_data[col].dtype}")
        
        # Check discount ranges
        discount_col = loaded_data['discount_offered']
        invalid_discounts = loaded_data[
            (discount_col < 0) | (discount_col > 100)
        ]
        print(f"✅ Discount range check: {len(invalid_discounts)} invalid discounts")
        
        # Check status values
        valid_statuses = ['accepted', 'rejected']
        invalid_statuses = loaded_data[~loaded_data['status'].isin(valid_statuses)]
        print(f"✅ Status check: {len(invalid_statuses)} invalid statuses")
        
        # Test full validation
        is_valid = processor.validate_data(loaded_data)
        print(f"\n🎯 Final validation result: {is_valid}")
        
        if not is_valid:
            print("❌ Validation failed - checking logs...")
            # Let's see if we can get more info
            return False
        
        # Test full processing
        processed_data = processor.process_data(data_file)
        print(f"✅ Full processing: {len(processed_data)} rows processed")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_data_processing()
