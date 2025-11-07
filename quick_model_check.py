#!/usr/bin/env python3
"""
Simple inline test to find working Gemini models
"""
import os
import sys

# Setup
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    print("🔍 Quick Gemini Model Check")
    print("-" * 30)
    
    # Check API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ No GEMINI_API_KEY found")
        return
    
    print(f"✅ API key found: {api_key[:10]}...")
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        # List models
        print("📋 Checking available models...")
        models = genai.list_models()
        
        working_models = []
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                model_name = model.name.replace('models/', '')
                working_models.append(model_name)
                print(f"  ✅ {model_name}")
        
        if working_models:
            # Test first model
            test_model = working_models[0]
            print(f"\n🧪 Testing {test_model}...")
            
            try:
                model = genai.GenerativeModel(test_model)
                response = model.generate_content("Say 'OK'")
                print(f"✅ {test_model} works: {response.text.strip()}")
                
                # Write the working model to a simple file for reference
                with open('working_model.txt', 'w') as f:
                    f.write(test_model)
                print(f"💾 Saved working model to working_model.txt")
                
            except Exception as e:
                print(f"❌ {test_model} failed: {e}")
        else:
            print("❌ No generative models found")
            
    except Exception as e:
        print(f"❌ API Error: {e}")

if __name__ == "__main__":
    main()
