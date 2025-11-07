#!/usr/bin/env python3
"""
Quick test for gemini-2.5-flash model
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

def test_gemini_2_5_flash():
    """Test specifically gemini-2.5-flash"""
    try:
        import google.generativeai as genai
        
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("❌ No GEMINI_API_KEY found")
            return False
        
        print(f"🔑 API Key: {api_key[:10]}...")
        
        genai.configure(api_key=api_key)
        
        print("🧪 Testing gemini-2.5-flash...")
        
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content("Respond with exactly: 'gemini-2.5-flash is working!'")
        
        print(f"✅ SUCCESS: {response.text.strip()}")
        return True
        
    except Exception as e:
        print(f"❌ Error with gemini-2.5-flash: {str(e)}")
        
        # If it fails, let's see what models are available
        try:
            print("\n📋 Checking available models...")
            models = genai.list_models()
            print("Available generative models:")
            for model in models:
                if 'generateContent' in model.supported_generation_methods:
                    model_name = model.name.replace('models/', '')
                    print(f"  ✅ {model_name}")
        except Exception as list_e:
            print(f"❌ Could not list models: {list_e}")
        
        return False

def test_updated_predictor():
    """Test the updated AI predictor with gemini-2.5-flash"""
    try:
        print("\n🔧 Testing updated AI predictor...")
        
        from ai_predictor import DiscountPredictor
        predictor = DiscountPredictor()
        
        if predictor.model and predictor.current_model_name:
            print(f"✅ Predictor using: {predictor.current_model_name}")
            return True
        else:
            print("❌ Predictor initialization failed")
            return False
            
    except Exception as e:
        print(f"❌ Predictor error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 TESTING GEMINI-2.5-FLASH")
    print("=" * 40)
    
    # Test direct API call
    direct_success = test_gemini_2_5_flash()
    
    # Test updated predictor
    predictor_success = test_updated_predictor()
    
    print("\n" + "=" * 40)
    print("📊 RESULTS:")
    print(f"Direct API: {'✅ WORKING' if direct_success else '❌ FAILED'}")
    print(f"AI Predictor: {'✅ WORKING' if predictor_success else '❌ FAILED'}")
    
    if direct_success and predictor_success:
        print("\n🎉 SUCCESS: gemini-2.5-flash is working!")
        print("✅ The AI predictions should work in Streamlit now")
    elif direct_success:
        print("\n⚠️  gemini-2.5-flash works but predictor has issues")
    else:
        print("\n❌ gemini-2.5-flash not available with this API key")
