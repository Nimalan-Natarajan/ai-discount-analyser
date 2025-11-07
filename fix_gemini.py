"""
Quick fix script for Gemini API model issues
This script will test your API key and find working models
"""
import sys
import os
sys.path.append('src')

def fix_gemini_api():
    print("🔧 Gemini API Quick Fix Tool")
    print("=" * 50)
    
    try:
        # Check environment
        from utils.config import Config
        import google.generativeai as genai
        
        if not Config.GEMINI_API_KEY:
            print("❌ No API key found in .env file")
            print("\n💡 Fix: Create/update your .env file with:")
            print("GEMINI_API_KEY=your_actual_api_key_here")
            return False
        
        print(f"✅ API key found: ...{Config.GEMINI_API_KEY[-8:]}")
        
        # Configure API
        genai.configure(api_key=Config.GEMINI_API_KEY)
        
        # Test different models
        working_models = []
        test_models = [
            'gemini-1.5-flash',
            'gemini-1.5-pro', 
            'gemini-1.0-pro',
            'gemini-pro'
        ]
        
        print("\n🧪 Testing available models...")
        
        for model_name in test_models:
            try:
                print(f"  Testing {model_name}...", end=" ")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content("Say 'OK' if you can respond.")
                
                if response and response.text:
                    print("✅ WORKS")
                    working_models.append(model_name)
                else:
                    print("❌ No response")
                    
            except Exception as e:
                error_msg = str(e)
                if "404" in error_msg or "not found" in error_msg:
                    print("❌ Not available")
                else:
                    print(f"❌ Error: {error_msg}")
        
        if working_models:
            print(f"\n🎉 Found {len(working_models)} working model(s):")
            for model in working_models:
                print(f"  ✅ {model}")
            
            # Update config recommendation
            best_model = working_models[0]
            print(f"\n💡 Recommended: Update ai_predictor.py to use '{best_model}'")
            
            # Offer to create a patch
            if input("\n🔄 Apply automatic fix? (y/N): ").lower().strip() == 'y':
                apply_fix(best_model)
            
            return True
        else:
            print("\n❌ No working models found!")
            print("\n🔍 Possible issues:")
            print("1. Invalid API key")
            print("2. API quota exceeded") 
            print("3. Regional restrictions")
            print("4. Billing not enabled")
            
            print("\n💡 Solutions:")
            print("1. Check your Google AI Studio account")
            print("2. Generate a new API key")
            print("3. Enable billing if required")
            
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False

def apply_fix(working_model):
    """Apply automatic fix to use working model"""
    try:
        ai_predictor_path = 'src/ai_predictor.py'
        
        # Read current file
        with open(ai_predictor_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Simple replacement for the model initialization
        old_lines = [
            "self.model = genai.GenerativeModel('gemini-pro')",
            "self.model = genai.GenerativeModel('gemini-1.5-flash')",
            "self.model = genai.GenerativeModel('gemini-1.5-pro')",
            "self.model = genai.GenerativeModel('gemini-1.0-pro')"
        ]
        
        new_line = f"self.model = genai.GenerativeModel('{working_model}')"
        
        updated = False
        for old_line in old_lines:
            if old_line in content:
                content = content.replace(old_line, new_line)
                updated = True
                break
        
        if updated:
            # Backup original
            backup_path = ai_predictor_path + '.backup'
            with open(backup_path, 'w', encoding='utf-8') as f:
                with open(ai_predictor_path, 'r', encoding='utf-8') as orig:
                    f.write(orig.read())
            
            # Write fixed version
            with open(ai_predictor_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Fixed! Updated ai_predictor.py to use '{working_model}'")
            print(f"📁 Backup saved as: {backup_path}")
        else:
            print("⚠️ Could not auto-fix. Manual update required.")
            
    except Exception as e:
        print(f"❌ Auto-fix failed: {str(e)}")

if __name__ == "__main__":
    fix_gemini_api()
