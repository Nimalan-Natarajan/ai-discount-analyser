"""
Simple test for the Gemini API fix
"""
import sys
import os
sys.path.append('src')

def test_gemini_fix():
    print("🧪 Testing Gemini API Fix...")
    
    try:
        # Clear any cached imports
        import importlib
        
        # Import fresh modules
        from utils.config import Config
        print(f"✅ Config imported, API key present: {bool(Config.GEMINI_API_KEY)}")
        
        # Test the AI predictor
        from ai_predictor import DiscountPredictor
        predictor = DiscountPredictor()
        
        print(f"✅ Predictor created, model loaded: {predictor.model is not None}")
        
        if predictor.model:
            # Test a simple prediction
            try:
                result = predictor.predict_discount_acceptance(
                    customer_id="CUST001",
                    lane_pair="usa_lax-germany_ham", 
                    shipment_type="air",
                    commodity_type="general",
                    proposed_discount=15.0
                )
                print(f"✅ Prediction test successful: {result['prediction']}")
                return True
            except Exception as pred_e:
                print(f"❌ Prediction test failed: {str(pred_e)}")
                return False
        else:
            print("❌ No model loaded")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_gemini_fix()
    if success:
        print("\n🎉 Gemini API fix successful!")
    else:
        print("\n❌ Fix needs more work")
