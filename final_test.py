"""
Final comprehensive test for Gemini API
"""
import os
import sys
sys.path.append('src')

def comprehensive_test():
    print("🔬 Comprehensive Gemini API Test")
    print("=" * 50)
    
    # Test 1: Check environment
    print("1️⃣ Environment Check...")
    try:
        from utils.config import Config
        api_key = Config.GEMINI_API_KEY
        if api_key:
            print(f"   ✅ API Key found: ...{api_key[-8:]}")
        else:
            print("   ❌ No API key in Config")
            return False
    except Exception as e:
        print(f"   ❌ Config error: {e}")
        return False
    
    # Test 2: Direct API test
    print("\n2️⃣ Direct API Test...")
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        # Test each model directly
        models_to_test = [
            'gemini-1.5-flash',
            'gemini-1.5-pro',
            'gemini-1.0-pro-latest', 
            'gemini-1.0-pro'
        ]
        
        working_model = None
        for model_name in models_to_test:
            try:
                print(f"   Testing {model_name}...", end=" ")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content("Hello")
                if response and response.text:
                    print("✅ WORKS")
                    working_model = model_name
                    break
                else:
                    print("❌ No response")
            except Exception as e:
                if "404" in str(e):
                    print("❌ Not found")
                else:
                    print(f"❌ {str(e)[:30]}...")
        
        if not working_model:
            print("   ❌ No working models found")
            return False
        
        print(f"   ✅ Working model: {working_model}")
    
    except Exception as e:
        print(f"   ❌ API test failed: {e}")
        return False
    
    # Test 3: AI Predictor test
    print("\n3️⃣ AI Predictor Test...")
    try:
        from ai_predictor import DiscountPredictor
        predictor = DiscountPredictor()
        
        if predictor.model:
            print(f"   ✅ Predictor loaded with model: {getattr(predictor, 'current_model_name', 'unknown')}")
            
            # Test prediction
            result = predictor.predict_discount_acceptance(
                customer_id="TEST",
                lane_pair="test-lane",
                shipment_type="air",
                commodity_type="general",
                proposed_discount=15.0
            )
            
            if result['prediction'] != 'unavailable':
                print(f"   ✅ Prediction works: {result['prediction']}")
                return True
            else:
                print(f"   ❌ Prediction unavailable: {result.get('reasoning', 'Unknown')}")
                return False
        else:
            print("   ❌ No model in predictor")
            return False
            
    except Exception as e:
        print(f"   ❌ Predictor test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = comprehensive_test()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 ALL TESTS PASSED! Gemini API is working correctly.")
        print("Your application should now work without the 404 error.")
    else:
        print("❌ Tests failed. The Gemini API needs attention.")
        print("\n💡 Possible solutions:")
        print("1. Check your API key is valid and active")
        print("2. Verify billing is enabled in Google Cloud")
        print("3. Try generating a new API key")
        
    print("\n🚀 Try launching the app with: python final_launcher.py")
