#!/usr/bin/env python3
"""
Test data format alignment between sample data and AI predictor
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import pandas as pd

def test_data_format_alignment():
    """Test that sample data format aligns with AI predictor expectations"""
    print("🔍 Testing Data Format Alignment...")
    
    # Load and process sample data
    try:
        from data_processor import QuoteProcessor
        from ai_predictor import DiscountPredictor
        
        processor = QuoteProcessor()
        sample_path = "data/sample_quotes.csv"
        
        if not os.path.exists(sample_path):
            print("❌ Sample data file not found")
            return False
        
        # Process the data
        print("📊 Processing sample data...")
        processed_data = processor.process_data(sample_path)
        print(f"✅ Processed {len(processed_data)} records")
        
        # Check processed data structure
        print("\n📋 Processed data columns:")
        for col in processed_data.columns:
            print(f"  • {col}")
        
        print(f"\n🔍 Sample processed data:")
        print(processed_data.head(3).to_string())
        
        # Test AI predictor with this data
        print("\n🤖 Testing AI predictor...")
        predictor = DiscountPredictor()
        predictor.load_historical_data(processed_data)
        
        # Test prediction with sample data values
        if len(processed_data) > 0:
            sample_row = processed_data.iloc[0]
            print(f"\n🧪 Testing prediction with sample row:")
            print(f"Customer: {sample_row['customer_id']}")
            print(f"Lane: {sample_row['lane_pair']}")
            print(f"Shipment: {sample_row['shipment_type']}")
            print(f"Commodity: {sample_row['commodity_type']}")
            
            # Test normalization
            norm_values = predictor._normalize_inputs(
                sample_row['customer_id'],
                sample_row['lane_pair'], 
                sample_row['shipment_type'],
                sample_row['commodity_type']
            )
            print(f"\n🔧 Normalized values:")
            print(f"Customer: {norm_values[0]}")
            print(f"Lane: {norm_values[1]}")
            print(f"Shipment: {norm_values[2]}")
            print(f"Commodity: {norm_values[3]}")
            
            return True
        else:
            print("❌ No processed data to test with")
            return False
            
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_upload_format_validation():
    """Test the expected upload format"""
    print("\n📤 Testing Upload Format Validation...")
    
    try:
        from data_processor import QuoteProcessor
        
        processor = QuoteProcessor()
        
        # Create a test CSV with the expected format
        test_data = {
            'customer_id': ['CUST001', 'CUST002'],
            'date': ['2024-01-15', '2024-01-20'],
            'shipment_type': ['AIR', 'OFR FCL'],
            'commodity_type': ['general', 'electronics'],
            'shipper_country': ['USA', 'China'],
            'shipper_station': ['LAX', 'SHA'],
            'consignee_country': ['Germany', 'USA'],
            'consignee_station': ['HAM', 'NYC'],
            'discount_offered': [15.5, 12.0],
            'status': ['accepted', 'rejected']
        }
        
        test_df = pd.DataFrame(test_data)
        print("✅ Test data created")
        
        # Validate the format
        is_valid = processor.validate_data(test_df)
        print(f"Validation result: {'✅ PASSED' if is_valid else '❌ FAILED'}")
        
        if is_valid:
            # Test processing
            cleaned_data = processor.clean_data(test_df)
            print(f"✅ Cleaned data: {len(cleaned_data)} records")
            print(f"Lane pairs created: {cleaned_data['lane_pair'].tolist()}")
            
        return is_valid
        
    except Exception as e:
        print(f"❌ Upload format test error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 DATA FORMAT ALIGNMENT TEST")
    print("=" * 50)
    
    # Test 1: Sample data processing
    sample_test = test_data_format_alignment()
    
    # Test 2: Upload format validation  
    upload_test = test_upload_format_validation()
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS:")
    print(f"Sample Data Processing: {'✅ PASSED' if sample_test else '❌ FAILED'}")
    print(f"Upload Format Validation: {'✅ PASSED' if upload_test else '❌ FAILED'}")
    
    if sample_test and upload_test:
        print("\n🎉 SUCCESS: Data format alignment is correct!")
        print("✅ Sample data and upload format are properly aligned")
        print("✅ AI predictor can handle the expected data format")
    else:
        print("\n⚠️  Some alignment issues detected")
        print("💡 Check the data processing pipeline")
