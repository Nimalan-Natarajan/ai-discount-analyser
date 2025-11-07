#!/usr/bin/env python3
"""
Diagnostic tool to check available Gemini models
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

def list_available_models():
    """List all available Gemini models for the current API key"""
    try:
        import google.generativeai as genai
        
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("❌ No GEMINI_API_KEY found in environment")
            return []
        
        print(f"🔑 Using API key: {api_key[:10]}...")
        
        # Configure the API
        genai.configure(api_key=api_key)
        
        print("📋 Listing all available models...")
        models = genai.list_models()
        
        available_models = []
        generative_models = []
        
        for model in models:
            model_name = model.name.replace('models/', '')
            available_models.append(model_name)
            
            if 'generateContent' in model.supported_generation_methods:
                generative_models.append(model_name)
                print(f"✅ {model_name} (supports generateContent)")
            else:
                print(f"ℹ️  {model_name} (other methods: {model.supported_generation_methods})")
        
        print(f"\n📊 Summary:")
        print(f"Total models: {len(available_models)}")
        print(f"Generative models: {len(generative_models)}")
        
        return generative_models
        
    except Exception as e:
        print(f"❌ Error listing models: {str(e)}")
        return []

def test_first_available_model(models):
    """Test the first available generative model"""
    if not models:
        print("❌ No generative models available to test")
        return False
    
    try:
        import google.generativeai as genai
        
        model_name = models[0]
        print(f"\n🧪 Testing first available model: {model_name}")
        
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Respond with exactly: 'Model working'")
        
        print(f"✅ Test successful: {response.text.strip()}")
        return True, model_name
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False, None

def update_predictor_with_working_model(working_model):
    """Update the AI predictor to use the working model"""
    if not working_model:
        return
    
    try:
        # Read current ai_predictor.py
        predictor_path = os.path.join('src', 'ai_predictor.py')
        with open(predictor_path, 'r') as f:
            content = f.read()
        
        # Find the WORKING_GEMINI_MODELS line and update it
        import re
        pattern = r'WORKING_GEMINI_MODELS\s*=\s*\[[^\]]*\]'
        new_models_list = f"WORKING_GEMINI_MODELS = ['{working_model}']"
        
        if re.search(pattern, content):
            updated_content = re.sub(pattern, new_models_list, content)
            
            with open(predictor_path, 'w') as f:
                f.write(updated_content)
            
            print(f"✅ Updated ai_predictor.py to use: {working_model}")
        else:
            print("⚠️  Could not find WORKING_GEMINI_MODELS in ai_predictor.py")
            
    except Exception as e:
        print(f"❌ Error updating predictor: {str(e)}")

if __name__ == "__main__":
    print("🔍 GEMINI MODEL DIAGNOSTIC")
    print("=" * 50)
    
    # Step 1: List all available models
    available_models = list_available_models()
    
    if available_models:
        print(f"\n🎯 Available generative models:")
        for i, model in enumerate(available_models, 1):
            print(f"{i}. {model}")
        
        # Step 2: Test the first available model
        success, working_model = test_first_available_model(available_models)
        
        if success:
            print(f"\n🔧 Updating application to use: {working_model}")
            update_predictor_with_working_model(working_model)
            
            print("\n🎉 SUCCESS!")
            print("✅ Found working model and updated the application")
            print("💡 Try using the AI Predictions feature now")
        else:
            print("\n❌ No working models found")
            print("💡 Check your API key permissions")
    else:
        print("\n❌ No models available")
        print("💡 Possible issues:")
        print("   - Invalid API key")
        print("   - API key lacks necessary permissions")
        print("   - Network connectivity issues")
        print("   - API service temporarily unavailable")
