#!/usr/bin/env python3
"""
Direct Gemini API test to resolve the 404 error
"""
import os
import sys
import logging

def test_gemini_api():
    """Test Gemini API with current working models"""
    
    print("🚀 Testing Gemini API...")
    
    # Check for API key
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment")
        return False
    
    print(f"✅ API key found: {api_key[:10]}...")
    
    try:
        import google.generativeai as genai
        print("✅ google.generativeai imported successfully")
        
        # Configure API
        genai.configure(api_key=api_key)
        print("✅ API configured")
        
        # List available models
        print("\n📋 Listing available models...")
        models = genai.list_models()
        available_models = []
        
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                model_name = model.name.replace('models/', '')
                available_models.append(model_name)
                print(f"  ✅ {model_name}")
        
        if not available_models:
            print("❌ No models with generateContent support found")
            return False
        
        # Test with first working model
        print(f"\n🧪 Testing with model: {available_models[0]}")
        
        try:
            model = genai.GenerativeModel(available_models[0])
            response = model.generate_content("Please respond with exactly: 'Gemini API is working correctly'")
            print(f"✅ Model response: {response.text.strip()}")
            
            return True
            
        except Exception as model_error:
            print(f"❌ Model test failed: {model_error}")
            
            # Try with a different model if available
            if len(available_models) > 1:
                print(f"🔄 Trying alternative model: {available_models[1]}")
                try:
                    model = genai.GenerativeModel(available_models[1])
                    response = model.generate_content("Please respond with exactly: 'Gemini API is working correctly'")
                    print(f"✅ Alternative model response: {response.text.strip()}")
                    return True
                except Exception as alt_error:
                    print(f"❌ Alternative model also failed: {alt_error}")
            
            return False
        
    except Exception as e:
        print(f"❌ Import or configuration error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🔧 GEMINI API DIAGNOSTIC TEST")
    print("=" * 60)
    
    success = test_gemini_api()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 SUCCESS: Gemini API is working correctly!")
        print("✅ You can now run the application with: python start_app.py")
    else:
        print("❌ FAILURE: Gemini API test failed")
        print("💡 Check your .env file and ensure GEMINI_API_KEY is valid")
    print("=" * 60)
