"""
AI-powered discount prediction using Google's Gemini API
"""
import google.generativeai as genai
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import json
import logging

try:
    from .utils.helpers import setup_logging, get_customer_history
    from .utils.config import Config
except ImportError:
    # Fallback for direct execution
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from utils.helpers import setup_logging, get_customer_history
    from utils.config import Config

# Define working models directly here to avoid any import issues
# Updated with most current Gemini model names as of Nov 2025
WORKING_GEMINI_MODELS = [
    'gemini-2.5-flash',          # Latest model as suggested
    'gemini-1.5-flash-latest',
    'gemini-1.5-pro-latest',
    'gemini-1.5-flash',
    'gemini-1.5-pro',
    'gemini-1.0-pro-latest',
    'gemini-1.0-pro-001',
    'gemini-1.0-pro'
]

class DiscountPredictor:
    """AI-powered discount prediction system"""
    
    def __init__(self):
        self.logger = setup_logging(Config.LOG_LEVEL)
        self.model = None
        self.historical_data = None
        self.current_model_name = None
        
        # Configure Gemini API - Check both Config and environment for API key
        import os
        api_key = Config.GEMINI_API_KEY or os.getenv('GEMINI_API_KEY')
        
        if api_key:
            try:
                genai.configure(api_key=api_key)
                self.model = None
                
                # First try hardcoded models
                models_to_try = WORKING_GEMINI_MODELS.copy()
                
                # If hardcoded models fail, try dynamic discovery
                if not self._try_models(models_to_try):
                    self.logger.info("Hardcoded models failed, trying dynamic discovery...")
                    discovered_models = self.discover_working_models()
                    if discovered_models:
                        self._try_models(discovered_models)
                
                if not self.model:
                    self.logger.error("❌ No working Gemini models found")
                    
            except Exception as e:
                self.logger.error(f"Failed to configure Gemini API: {str(e)}")
                self.model = None
        else:
            self.logger.warning("Gemini API key not found. AI predictions will be unavailable.")
    
    def _try_models(self, models_list):
        """Try a list of models and return True if one works"""
        for model_name in models_list:
            try:
                self.logger.info(f"Attempting to load model: {model_name}")
                test_model = genai.GenerativeModel(model_name)
                
                # Set the model without testing during init (to avoid quota usage)
                self.model = test_model
                self.current_model_name = model_name
                self.logger.info(f"✅ Successfully configured Gemini API with {model_name}")
                return True
                
            except Exception as model_e:
                error_msg = str(model_e)
                if "404" in error_msg or "not found" in error_msg:
                    self.logger.info(f"❌ Model {model_name} not available (404)")
                else:
                    self.logger.warning(f"❌ Model {model_name} error: {error_msg}")
                continue
        
        return False
    
    def load_historical_data(self, df: pd.DataFrame) -> None:
        """Load historical quote data for context"""
        self.historical_data = df.copy()
        self.logger.info(f"Loaded {len(df)} historical records")
    
    def _normalize_inputs(self, customer_id: str, lane_pair: str, 
                         shipment_type: str, commodity_type: str) -> tuple:
        """Normalize input values to match the processed data format"""
        # Convert to lowercase to match processed data format
        normalized_shipment_type = shipment_type.lower().strip()
        normalized_commodity_type = commodity_type.lower().strip()
        normalized_customer_id = customer_id.upper().strip()  # Keep customer IDs uppercase
        
        # Normalize lane_pair format (the data processor creates lowercase with underscores)
        # Convert "USA-LAX to Germany-HAM" to "usa_lax-germany_ham"
        if " to " in lane_pair:
            parts = lane_pair.split(" to ")
            if len(parts) == 2:
                origin = parts[0].replace("-", "_").lower()
                destination = parts[1].replace("-", "_").lower()
                normalized_lane_pair = f"{origin}-{destination}"
            else:
                normalized_lane_pair = lane_pair.lower()
        else:
            normalized_lane_pair = lane_pair.lower()
        
        return normalized_customer_id, normalized_lane_pair, normalized_shipment_type, normalized_commodity_type
    
    def prepare_context(self, customer_id: str, lane_pair: str, 
                       shipment_type: str, commodity_type: str) -> str:
        """Prepare context for AI prediction"""
        if self.historical_data is None:
            return "No historical data available."
        
        # Get customer history
        customer_history = get_customer_history(self.historical_data, customer_id)
        
        # Get lane-specific data (lane_pair should already be normalized)
        lane_data = self.historical_data[
            self.historical_data['lane_pair'] == lane_pair
        ]
        
        # Get shipment type data
        shipment_data = self.historical_data[
            self.historical_data['shipment_type'] == shipment_type
        ]
        
        # Get commodity type data
        commodity_data = self.historical_data[
            self.historical_data['commodity_type'] == commodity_type
        ]
        
        context = f"""
        LOGISTICS QUOTE ANALYSIS CONTEXT:
        
        Customer Analysis (ID: {customer_id}):
        - Total historical quotes: {customer_history.get('total_quotes', 0)}
        - Acceptance rate: {customer_history.get('acceptance_rate', 0):.1%}
        - Average accepted discount: {customer_history.get('average_accepted_discount', 0):.1f}%
        
        Lane Analysis ({lane_pair}):
        - Total quotes for this lane: {len(lane_data)}
        - Lane acceptance rate: {(lane_data['status'] == 'accepted').mean():.1%}
        - Average discount for this lane: {lane_data['discount_offered'].mean():.1f}%
        
        Shipment Type Analysis ({shipment_type}):
        - Total quotes for this shipment type: {len(shipment_data)}
        - Shipment type acceptance rate: {(shipment_data['status'] == 'accepted').mean():.1%}
        - Average discount for this shipment type: {shipment_data['discount_offered'].mean():.1f}%
        
        Commodity Analysis ({commodity_type}):
        - Total quotes for this commodity: {len(commodity_data)}
        - Commodity acceptance rate: {(commodity_data['status'] == 'accepted').mean():.1%}
        - Average discount for this commodity: {commodity_data['discount_offered'].mean():.1f}%
        """
        
        return context
    
    def predict_discount_acceptance(self, customer_id: str, lane_pair: str,
                                  shipment_type: str, commodity_type: str,
                                  proposed_discount: float) -> Dict[str, Any]:
        """Predict likelihood of discount acceptance using AI"""
        if not self.model:
            # Try to reinitialize if model failed during startup
            self.__init__()
            if not self.model:
                return {
                    'prediction': 'unavailable',
                    'confidence': 0,
                    'reasoning': 'Gemini API not configured or no working models available',
                    'recommended_discount': proposed_discount,
                    'key_factors': [],
                    'risk_assessment': 'unknown'
                }
        
        try:
            # Normalize inputs to match processed data format
            norm_customer_id, norm_lane_pair, norm_shipment_type, norm_commodity_type = \
                self._normalize_inputs(customer_id, lane_pair, shipment_type, commodity_type)
            
            # Prepare context
            context = self.prepare_context(norm_customer_id, norm_lane_pair, norm_shipment_type, norm_commodity_type)
            
            # Create prediction prompt
            prompt = f"""
            You are an expert logistics pricing analyst. Based on the historical data provided, 
            predict the likelihood that a customer will accept a discount offer.
            
            {context}
            
            CURRENT QUOTE DETAILS:
            - Customer ID: {norm_customer_id}
            - Lane: {norm_lane_pair} (Original: {lane_pair})
            - Shipment Type: {norm_shipment_type} (Original: {shipment_type})
            - Commodity Type: {norm_commodity_type} (Original: {commodity_type})
            - Proposed Discount: {proposed_discount}%
            
            Please provide your analysis in the following JSON format:
            {{
                "acceptance_probability": <float between 0 and 1>,
                "confidence_level": <float between 0 and 1>,
                "key_factors": [<list of key factors influencing the decision>],
                "recommended_discount": <suggested optimal discount percentage>,
                "reasoning": "<detailed explanation of your analysis>",
                "risk_assessment": "<low/medium/high>"
            }}
            
            Consider factors such as:
            - Customer's historical acceptance patterns
            - Lane-specific pricing trends
            - Shipment type preferences
            - Commodity type considerations
            - Seasonal factors
            - Market conditions
            """
            
            # Get AI prediction
            response = self.model.generate_content(prompt)
            
            # Parse response
            try:
                # Extract JSON from response
                response_text = response.text
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                json_str = response_text[json_start:json_end]
                
                prediction_data = json.loads(json_str)
                
                return {
                    'prediction': 'likely' if prediction_data.get('acceptance_probability', 0) > 0.5 else 'unlikely',
                    'probability': prediction_data.get('acceptance_probability', 0),
                    'confidence': prediction_data.get('confidence_level', 0),
                    'reasoning': prediction_data.get('reasoning', ''),
                    'recommended_discount': prediction_data.get('recommended_discount', proposed_discount),
                    'key_factors': prediction_data.get('key_factors', []),
                    'risk_assessment': prediction_data.get('risk_assessment', 'medium')
                }
                
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                return {
                    'prediction': 'uncertain',
                    'probability': 0.5,
                    'confidence': 0.3,
                    'reasoning': response.text,
                    'recommended_discount': proposed_discount,
                    'key_factors': [],
                    'risk_assessment': 'medium'
                }
        
        except Exception as e:
            self.logger.error(f"Error in AI prediction: {str(e)}")
            return {
                'prediction': 'error',
                'probability': 0,
                'confidence': 0,
                'reasoning': f'Error occurred: {str(e)}',
                'recommended_discount': proposed_discount,
                'key_factors': [],
                'risk_assessment': 'high'
            }
    
    def batch_predict(self, quotes_df: pd.DataFrame) -> pd.DataFrame:
        """Perform batch predictions on multiple quotes"""
        results = []
        
        for _, row in quotes_df.iterrows():
            prediction = self.predict_discount_acceptance(
                customer_id=row['customer_id'],
                lane_pair=row['lane_pair'],
                shipment_type=row['shipment_type'],
                commodity_type=row['commodity_type'],
                proposed_discount=row['discount_offered']
            )
            
            results.append({
                'customer_id': row['customer_id'],
                'lane_pair': row['lane_pair'],
                'predicted_acceptance': prediction['prediction'],
                'acceptance_probability': prediction['probability'],
                'confidence': prediction['confidence'],
                'recommended_discount': prediction['recommended_discount'],
                'risk_assessment': prediction['risk_assessment']
            })
        
        return pd.DataFrame(results)
    
    def get_optimal_discount_suggestions(self, customer_id: str, lane_pair: str,
                                       shipment_type: str, commodity_type: str,
                                       discount_range: tuple = (0, 30)) -> Dict[str, Any]:
        """Get optimal discount suggestions with improved efficiency"""
        if not self.model:
            return {'error': 'AI model not available'}
        
        min_discount, max_discount = discount_range
        
        # Use fewer test points for faster results (5% increments instead of 2.5%)
        test_discounts = np.arange(min_discount, max_discount + 1, 5.0)
        
        # If range is small, use more granular testing
        if max_discount - min_discount <= 15:
            test_discounts = np.arange(min_discount, max_discount + 1, 2.5)
        
        predictions = []
        for discount in test_discounts:
            pred = self.predict_discount_acceptance(
                customer_id, lane_pair, shipment_type, commodity_type, discount
            )
            predictions.append({
                'discount': discount,
                'probability': pred['probability'],
                'confidence': pred['confidence']
            })
        
        # Find optimal discount (highest probability with reasonable confidence)
        valid_predictions = [p for p in predictions if p['confidence'] > 0.5]
        if valid_predictions:
            optimal = max(valid_predictions, key=lambda x: x['probability'])
            return {
                'optimal_discount': optimal['discount'],
                'success_probability': optimal['probability'],
                'confidence': optimal['confidence'],
                'all_predictions': predictions
            }
        
        return {
            'optimal_discount': (min_discount + max_discount) / 2,
            'success_probability': 0.5,
            'confidence': 0.3,
            'all_predictions': predictions
        }
    
    def get_static_discount_analysis(self, customer_id: str, lane_pair: str,
                                   shipment_type: str, commodity_type: str,
                                   discount_range: tuple = (0, 30)) -> Dict[str, Any]:
        """Get discount analysis based on historical data only (faster, no AI calls)"""
        if self.historical_data is None:
            return {'error': 'No historical data available'}
        
        # Normalize inputs
        norm_customer_id, norm_lane_pair, norm_shipment_type, norm_commodity_type = \
            self._normalize_inputs(customer_id, lane_pair, shipment_type, commodity_type)
        
        # Filter historical data for similar scenarios
        similar_data = self.historical_data[
            (self.historical_data['customer_id'] == norm_customer_id) |
            (self.historical_data['lane_pair'] == norm_lane_pair) |
            (self.historical_data['shipment_type'] == norm_shipment_type) |
            (self.historical_data['commodity_type'] == norm_commodity_type)
        ]
        
        if similar_data.empty:
            # Fall back to overall data
            similar_data = self.historical_data
        
        # Analyze accepted quotes only
        accepted_data = similar_data[similar_data['status'] == 'accepted']
        
        if accepted_data.empty:
            return {
                'error': 'No accepted quotes found for similar scenarios',
                'recommendation': 'Consider using AI predictions for this scenario'
            }
        
        # Calculate statistics
        min_discount, max_discount = discount_range
        avg_discount = accepted_data['discount_offered'].mean()
        median_discount = accepted_data['discount_offered'].median()
        success_rate = len(accepted_data) / len(similar_data)
        
        # Find optimal range based on historical data
        optimal_discount = min(max(avg_discount, min_discount), max_discount)
        
        return {
            'method': 'static_analysis',
            'optimal_discount': optimal_discount,
            'success_probability': success_rate,
            'confidence': 0.8 if len(accepted_data) > 5 else 0.6,
            'historical_stats': {
                'total_similar_quotes': len(similar_data),
                'accepted_quotes': len(accepted_data),
                'average_accepted_discount': avg_discount,
                'median_accepted_discount': median_discount,
                'min_accepted_discount': accepted_data['discount_offered'].min(),
                'max_accepted_discount': accepted_data['discount_offered'].max()
            },
            'recommendation': f"Based on {len(accepted_data)} similar accepted quotes"
        }
    
    def discover_working_models(self) -> List[str]:
        """Dynamically discover available Gemini models"""
        try:
            if not Config.GEMINI_API_KEY:
                return []
            
            self.logger.info("Discovering available Gemini models...")
            models = genai.list_models()
            available_models = []
            
            for model in models:
                if 'generateContent' in model.supported_generation_methods:
                    model_name = model.name.replace('models/', '')
                    available_models.append(model_name)
                    self.logger.info(f"Found generative model: {model_name}")
            
            return available_models
            
        except Exception as e:
            self.logger.error(f"Error discovering models: {str(e)}")
            return []
    
    def list_available_models(self) -> List[str]:
        """List available Gemini models for debugging"""
        try:
            if not Config.GEMINI_API_KEY:
                return ["No API key configured"]
            
            models = genai.list_models()
            available_models = []
            for model in models:
                if 'generateContent' in model.supported_generation_methods:
                    available_models.append(model.name)
            
            self.logger.info(f"Available models: {available_models}")
            return available_models
            
        except Exception as e:
            self.logger.error(f"Error listing models: {str(e)}")
            return [f"Error: {str(e)}"]
    
    def test_api_connection(self):
        """Test if the API key is working by making a simple request"""
        try:
            if not self.model:
                return False, "No model configured"
            
            # Make a simple test request
            response = self.model.generate_content("Test")
            
            if response and response.text:
                return True, "API connection successful"
            else:
                return False, "API request failed - no response"
                
        except Exception as e:
            error_msg = str(e)
            if "403" in error_msg:
                return False, "API key invalid or permission denied (403)"
            elif "404" in error_msg:
                return False, "Model not found (404)"
            elif "quota" in error_msg.lower():
                return False, "API quota exceeded"
            else:
                return False, f"API error: {error_msg}"
    
    def reinitialize_with_api_key(self, api_key):
        """Reinitialize the predictor with a new API key"""
        try:
            genai.configure(api_key=api_key)
            self.model = None
            self.current_model_name = None
            
            # First try hardcoded models
            models_to_try = WORKING_GEMINI_MODELS.copy()
            
            # If hardcoded models fail, try dynamic discovery
            if not self._try_models(models_to_try):
                self.logger.info("Hardcoded models failed, trying dynamic discovery...")
                discovered_models = self.discover_working_models()
                if discovered_models:
                    self._try_models(discovered_models)
            
            if self.model:
                self.logger.info(f"✅ Successfully reinitialized with model {self.current_model_name}")
                return True
            else:
                self.logger.error("❌ Failed to initialize any working model")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to reinitialize with new API key: {str(e)}")
            return False
    
    def test_api_connection(self):
        """Test if the API key is working by making a simple request"""
        try:
            if not self.model:
                return False, "No model configured"
            
            # Make a simple test request
            response = self.model.generate_content("Test")
            
            if response and response.text:
                return True, "API connection successful"
            else:
                return False, "API request failed - no response"
                
        except Exception as e:
            error_msg = str(e)
            if "403" in error_msg:
                return False, "API key invalid or permission denied (403)"
            elif "404" in error_msg:
                return False, "Model not found (404)"
            elif "quota" in error_msg.lower():
                return False, "API quota exceeded"
            else:
                return False, f"API error: {error_msg}"
    
    def reinitialize_with_api_key(self, api_key):
        """Reinitialize the predictor with a new API key"""
        try:
            genai.configure(api_key=api_key)
            self.model = None
            self.current_model_name = None
            
            # First try hardcoded models
            models_to_try = WORKING_GEMINI_MODELS.copy()
            
            # If hardcoded models fail, try dynamic discovery
            if not self._try_models(models_to_try):
                self.logger.info("Hardcoded models failed, trying dynamic discovery...")
                discovered_models = self.discover_working_models()
                if discovered_models:
                    self._try_models(discovered_models)
            
            if self.model:
                self.logger.info(f"✅ Successfully reinitialized with model {self.current_model_name}")
                return True
            else:
                self.logger.error("❌ Failed to initialize any working model")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to reinitialize with new API key: {str(e)}")
            return False
