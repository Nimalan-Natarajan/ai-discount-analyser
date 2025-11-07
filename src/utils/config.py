"""
Configuration settings for the Logistics Quotation Management Tool
"""
import os

# Try to load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # If python-dotenv is not available, just use os.environ
    pass

class Config:
    """Application configuration"""
    
    # API Keys
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # Application Settings
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Data Paths
    DATA_DIR = 'data'
    PROCESSED_DATA_DIR = 'data/processed'
    
    # Shipment Types
    SHIPMENT_TYPES = ['AIR', 'OFR FCL', 'OFR LCL']
    
    # Commodity Types
    COMMODITY_TYPES = [
        'general',
        'temperature-sensitive',
        'dangerous goods',
        'perishables',
        'electronics',
        'automotive',
        'textiles',
        'machinery'
    ]
    
    # Model Configuration
    MODEL_CONFIG = {
        'test_size': 0.2,
        'random_state': 42,
        'cv_folds': 5
    }
    
    # Gemini Model Configuration
    GEMINI_MODELS = [
        'gemini-2.5-flash',      # Latest and fastest
        'gemini-1.5-flash',      # Fast and efficient
        'gemini-1.5-pro',        # More capable
        'gemini-1.0-pro-latest', # Fallback option
        'gemini-1.0-pro'         # Legacy fallback
    ]
    
    # Streamlit Configuration
    STREAMLIT_CONFIG = {
        'page_title': 'AI-Driven Discount Analyser Tool',
        'page_icon': '🚢',
        'layout': 'wide'
    }
