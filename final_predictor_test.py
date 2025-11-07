#!/usr/bin/env python3
"""
Test the updated AI predictor with dynamic model discovery
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_updated_predictor():
    """Test the AI predictor with new dynamic discovery"""
    try:
        print("🔧 Testing updated AI predictor...")
        
        from ai_predictor import DiscountPredictor
        
        # Create predictor (should try multiple models now)
        predictor = DiscountPredictor()
        
        if predictor.model and predictor.current_model_name:
            print(f"✅ Success! Using model: {predictor.current_model_name}")
            
            # Test a simple prediction
            try:
                result = predictor.predict_discount_acceptance(
                    customer_id="TEST001",
                    lane_pair="USA-LAX to China-SHA", 
                    shipment_type="AIR",
                    commodity_type="general",
                    proposed_discount=15.0
                )
                
                if result['prediction'] != 'error':
                    print(f"✅ Prediction test passed: {result['prediction']}")
                    return True
                else:
                    print(f"⚠️  Prediction returned error: {result['reasoning']}")
                    return False
                    
            except Exception as pred_e:
                print(f"⚠️  Prediction test failed: {pred_e}")
                return False
        else:
            print("❌ AI predictor failed to initialize")
            
            # Try to get available models for debugging
            available = predictor.list_available_models()
            print(f"Available models: {available}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing predictor: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 TESTING UPDATED AI PREDICTOR")
    print("=" * 40)
    
    success = test_updated_predictor()
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 SUCCESS: AI predictor is working!")
        print("✅ The Gemini API issue should be resolved")
        print("💡 Try the AI Predictions feature in Streamlit now")
    else:
        print("❌ AI predictor still has issues")
        print("💡 Check your .env file for a valid GEMINI_API_KEY")
