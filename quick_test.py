"""
Quick test to check Gemini API status
"""
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv('GEMINI_API_KEY')
print(f"API Key found: {'Yes' if api_key else 'No'}")

if api_key:
    try:
        # Configure API
        genai.configure(api_key=api_key)
        print("✅ API configured successfully")
        
        # List available models
        print("\n📋 Available models:")
        models = genai.list_models()
        available_models = []
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                print(f"  - {model.name}")
                available_models.append(model.name)
        
        # Test with the first available model
        if available_models:
            test_model_name = available_models[0].replace('models/', '')
            print(f"\n🧪 Testing model: {test_model_name}")
            
            model = genai.GenerativeModel(test_model_name)
            response = model.generate_content("Hello, can you respond with just 'API working'?")
            print(f"✅ Response: {response.text}")
            
        else:
            print("❌ No models with generateContent support found")
            
    except Exception as e:
        print(f"❌ Error: {e}")
else:
    print("❌ No API key found in environment")
