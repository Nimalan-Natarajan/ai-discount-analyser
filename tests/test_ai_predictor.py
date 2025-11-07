"""
Tests for AI predictor module
"""
import pytest
import pandas as pd
import numpy as np
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from ai_predictor import DiscountPredictor

class TestDiscountPredictor:
    """Test cases for DiscountPredictor class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.predictor = DiscountPredictor()
        
        # Create sample historical data
        self.sample_data = pd.DataFrame({
            'customer_id': ['CUST001', 'CUST002', 'CUST001', 'CUST002'],
            'date': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04']),
            'shipment_type': ['air', 'ofr fcl', 'air', 'ofr lcl'],
            'commodity_type': ['general', 'electronics', 'textiles', 'general'],
            'shipper_country': ['usa', 'china', 'usa', 'china'],
            'shipper_station': ['lax', 'sha', 'lax', 'sha'],
            'consignee_country': ['germany', 'usa', 'japan', 'germany'],
            'consignee_station': ['ham', 'nyc', 'nrt', 'ham'],
            'discount_offered': [15.0, 12.0, 18.5, 20.0],
            'status': ['accepted', 'rejected', 'accepted', 'accepted'],
            'lane_pair': ['usa_lax-germany_ham', 'china_sha-usa_nyc', 'usa_lax-japan_nrt', 'china_sha-germany_ham']
        })
    
    def test_load_historical_data(self):
        """Test loading historical data"""
        self.predictor.load_historical_data(self.sample_data)
        
        assert self.predictor.historical_data is not None
        assert len(self.predictor.historical_data) == 4
    
    def test_prepare_context(self):
        """Test context preparation for AI prediction"""
        self.predictor.load_historical_data(self.sample_data)
        
        context = self.predictor.prepare_context(
            customer_id='CUST001',
            lane_pair='usa_lax-germany_ham',
            shipment_type='air',
            commodity_type='general'
        )
        
        assert isinstance(context, str)
        assert 'CUST001' in context
        assert 'usa_lax-germany_ham' in context
    
    def test_predict_discount_acceptance_no_api(self):
        """Test prediction when API is not configured"""
        # Ensure predictor has no model (simulating no API key)
        self.predictor.model = None
        
        prediction = self.predictor.predict_discount_acceptance(
            customer_id='CUST001',
            lane_pair='usa_lax-germany_ham',
            shipment_type='air',
            commodity_type='general',
            proposed_discount=15.0
        )
        
        assert prediction['prediction'] == 'unavailable'
        assert prediction['confidence'] == 0
        assert 'not configured' in prediction['reasoning']
    
    def test_batch_predict(self):
        """Test batch prediction functionality"""
        # Mock predict_discount_acceptance to avoid API calls
        original_method = self.predictor.predict_discount_acceptance
        
        def mock_predict(customer_id, lane_pair, shipment_type, commodity_type, proposed_discount):
            return {
                'prediction': 'likely',
                'probability': 0.7,
                'confidence': 0.8,
                'recommended_discount': proposed_discount,
                'risk_assessment': 'low'
            }
        
        self.predictor.predict_discount_acceptance = mock_predict
        
        # Test batch prediction
        test_data = self.sample_data[['customer_id', 'lane_pair', 'shipment_type', 'commodity_type', 'discount_offered']].head(2)
        results = self.predictor.batch_predict(test_data)
        
        assert len(results) == 2
        assert 'predicted_acceptance' in results.columns
        assert 'acceptance_probability' in results.columns
        
        # Restore original method
        self.predictor.predict_discount_acceptance = original_method
    
    def test_get_optimal_discount_suggestions_no_api(self):
        """Test optimal discount suggestions when API is not configured"""
        self.predictor.model = None
        
        suggestions = self.predictor.get_optimal_discount_suggestions(
            customer_id='CUST001',
            lane_pair='usa_lax-germany_ham',
            shipment_type='air',
            commodity_type='general'
        )
        
        assert 'error' in suggestions
        assert suggestions['error'] == 'AI model not available'
