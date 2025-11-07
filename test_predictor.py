"""
Simple test of AI predictor to debug the Gemini API issue
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from ai_predictor import DiscountPredictor
    
    print("🚀 Testing DiscountPredictor initialization...")
    predictor = DiscountPredictor()
    
    if predictor.model:
        print(f"✅ AI Predictor initialized successfully with model: {getattr(predictor, 'current_model_name', 'unknown')}")
        
        # Test available models method
        available = predictor.list_available_models()
        print(f"📋 Available models: {available}")
        
    else:
        print("❌ AI Predictor initialization failed - no model available")
        
except Exception as e:
    print(f"❌ Error initializing AI Predictor: {e}")
    import traceback
    traceback.print_exc()
