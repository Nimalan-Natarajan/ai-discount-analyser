"""
Test script to verify Gemini API configuration and available models
"""
import sys
import os
sys.path.append('src')

def test_gemini_api():
    print("🔧 Testing Gemini API Configuration...")
    
    try:
        # Test imports
        import google.generativeai as genai
        from utils.config import Config
        print("✅ Imports successful")
        
        # Check API key
        if not Config.GEMINI_API_KEY:
            print("❌ GEMINI_API_KEY not found in .env file")
            return False
        
        print(f"✅ API Key found (ends with: ...{Config.GEMINI_API_KEY[-8:]})")
        
        # Configure API
        genai.configure(api_key=Config.GEMINI_API_KEY)
        print("✅ API configured")
        
        # List available models
        print("\n📋 Listing available models...")
        try:
            models = genai.list_models()
            available_models = []
            for model in models:
                if 'generateContent' in model.supported_generation_methods:
                    available_models.append(model.name)
                    print(f"  ✅ {model.name}")
            
            if not available_models:
                print("❌ No models available for content generation")
                return False
                
        except Exception as e:
            print(f"❌ Error listing models: {str(e)}")
            return False
        
        # Test the current model
        print(f"\n🧪 Testing gemini-1.5-flash model...")
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Simple test
            response = model.generate_content("Say 'Hello, API test successful!' in a professional tone.")
            print(f"✅ Model response: {response.text}")
            
        except Exception as e:
            print(f"❌ Model test failed: {str(e)}")
            
            # Try alternative models
            print("🔄 Trying alternative models...")
            for model_name in ['gemini-1.5-pro', 'gemini-1.0-pro']:
                try:
                    print(f"  Testing {model_name}...")
                    alt_model = genai.GenerativeModel(model_name)
                    response = alt_model.generate_content("Say 'Hello!' briefly.")
                    print(f"  ✅ {model_name} works: {response.text[:50]}...")
                    
                    # Update the config with working model
                    print(f"💡 Consider updating ai_predictor.py to use '{model_name}'")
                    break
                except Exception as alt_e:
                    print(f"  ❌ {model_name} failed: {str(alt_e)}")
            
            return False
        
        print("\n🎉 Gemini API is working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing Gemini API: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_gemini_api()
