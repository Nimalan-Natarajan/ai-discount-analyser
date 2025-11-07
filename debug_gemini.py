#!/usr/bin/env python3
"""
Verify the Gemini API fix is working correctly
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

def test_gemini_api():
    """Test Gemini API with working models"""
    try:
        import google.generativeai as genai
        
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            return False, "No API key found"
        
        genai.configure(api_key=api_key)
        
        # Test with gemini-1.5-flash (should be available)
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content("Respond with just 'API OK'")
            return True, f"Success: {response.text.strip()}"
        except Exception as e:
            return False, f"API Error: {str(e)}"
            
    except Exception as e:
        return False, f"Setup Error: {str(e)}"

def test_ai_predictor():
    """Test our AI predictor"""
    try:
        from ai_predictor import DiscountPredictor
        predictor = DiscountPredictor()
        
        if predictor.model and hasattr(predictor, 'current_model_name'):
            return True, f"Predictor OK with {predictor.current_model_name}"
        else:
            return False, "Predictor initialization failed"
            
    except Exception as e:
        return False, f"Predictor Error: {str(e)}"

def debug_gemini_input():
    """Debug what data is being sent to Gemini API"""
    print("\n🔍 **GEMINI API INPUT DEBUGGER**")
    print("=" * 50)
    
    try:
        from ai_predictor import DiscountPredictor
        from data_processor import QuoteProcessor
        
        # Load test data
        processor = QuoteProcessor()
        
        if os.path.exists("test_quotes.csv"):
            print("\n📊 Loading test_quotes.csv...")
            data = processor.load_data("test_quotes.csv")
            print(f"✅ Loaded {len(data)} records")
            
            # Initialize predictor with data
            predictor = DiscountPredictor()
            predictor.load_historical_data(data)
            
            # Test prediction with sample data
            print("\n🧪 **TESTING PREDICTION REQUEST**")
            print("-" * 30)
            
            # Use first row as test case
            test_row = data.iloc[0]
            customer_id = test_row['customer_id']
            
            # Create lane pair from the row
            lane_pair = f"{test_row['shipper_country']}-{test_row['shipper_station']} to {test_row['consignee_country']}-{test_row['consignee_station']}"
            shipment_type = test_row['shipment_type']
            commodity_type = test_row['commodity_type']
            proposed_discount = float(test_row['discount_offered'])
            
            print(f"🎯 **TEST CASE:**")
            print(f"   Customer ID: {customer_id}")
            print(f"   Lane Pair: {lane_pair}")
            print(f"   Shipment Type: {shipment_type}")
            print(f"   Commodity Type: {commodity_type}")
            print(f"   Proposed Discount: {proposed_discount}%")
            
            # Get the context that would be sent to Gemini
            print(f"\n📝 **CONTEXT SENT TO GEMINI:**")
            print("=" * 40)
            
            context = predictor._build_context(customer_id, lane_pair, shipment_type, commodity_type)
            print(context)
            
            print(f"\n🚀 **WHAT GEMINI RECEIVES:**")
            print("1. Historical customer data analysis")
            print("2. Lane-specific acceptance patterns") 
            print("3. Shipment type preferences")
            print("4. Commodity-specific trends")
            print("5. Current quote details for prediction")
            print("\nGemini analyzes all this data to predict acceptance probability!")
            
        else:
            print("❌ test_quotes.csv not found")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🔧 Testing Gemini API Fix...")
    
    api_ok, api_msg = test_gemini_api()
    pred_ok, pred_msg = test_ai_predictor()
    
    print(f"API Test: {'✅' if api_ok else '❌'} {api_msg}")
    print(f"Predictor Test: {'✅' if pred_ok else '❌'} {pred_msg}")
    
    if api_ok and pred_ok:
        print("\n🎉 SUCCESS: Gemini API fix is working!")
        print("✅ The 404 error should be resolved")
        
        # Also run the input debugger
        debug_gemini_input()
    else:
        print("\n⚠️  Some issues detected - check your .env file")
