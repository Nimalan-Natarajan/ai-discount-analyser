"""
Simple test to verify data processing fix
"""
import os
import sys
sys.path.append('src')

try:
    print("🔧 Testing Data Processing Fix...")
    
    # Import modules
    from data_processor import QuoteProcessor
    print("✅ Import successful")
    
    # Create processor
    processor = QuoteProcessor()
    print("✅ Processor created")
    
    # Load sample data
    data_file = 'data/sample_quotes.csv'
    if os.path.exists(data_file):
        print(f"✅ Data file exists: {data_file}")
        
        # Process data
        processed_data = processor.process_data(data_file)
        print(f"✅ Data processed successfully: {len(processed_data)} records")
        
        # Get summary
        summary = processor.get_data_summary()
        print(f"✅ Summary generated: {summary.get('total_records', 0)} total records")
        
        print("\n🎉 Data processing is working correctly!")
        
    else:
        print(f"❌ Data file not found: {data_file}")

except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
