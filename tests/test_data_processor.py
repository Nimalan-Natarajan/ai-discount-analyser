"""
Tests for data processor module
"""
import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_processor import QuoteProcessor

class TestQuoteProcessor:
    """Test cases for QuoteProcessor class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.processor = QuoteProcessor()
        
        # Create sample data
        self.sample_data = pd.DataFrame({
            'customer_id': ['CUST001', 'CUST002', 'CUST001'],
            'date': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'shipment_type': ['AIR', 'OFR FCL', 'AIR'],
            'commodity_type': ['general', 'electronics', 'textiles'],
            'shipper_country': ['USA', 'China', 'USA'],
            'shipper_station': ['LAX', 'SHA', 'LAX'],
            'consignee_country': ['Germany', 'USA', 'Japan'],
            'consignee_station': ['HAM', 'NYC', 'NRT'],
            'discount_offered': [15.0, 12.0, 18.5],
            'status': ['accepted', 'rejected', 'accepted']
        })
    
    def test_validate_data_valid(self):
        """Test data validation with valid data"""
        assert self.processor.validate_data(self.sample_data) == True
    
    def test_validate_data_missing_columns(self):
        """Test data validation with missing columns"""
        invalid_data = self.sample_data.drop('customer_id', axis=1)
        assert self.processor.validate_data(invalid_data) == False
    
    def test_validate_data_empty(self):
        """Test data validation with empty dataframe"""
        empty_data = pd.DataFrame()
        assert self.processor.validate_data(empty_data) == False
    
    def test_clean_data(self):
        """Test data cleaning functionality"""
        cleaned_data = self.processor.clean_data(self.sample_data)
        
        # Check if date column is datetime
        assert pd.api.types.is_datetime64_any_dtype(cleaned_data['date'])
        
        # Check if lane_pair column is created
        assert 'lane_pair' in cleaned_data.columns
        
        # Check if text columns are lowercase
        assert all(cleaned_data['status'].str.islower())
    
    def test_create_features(self):
        """Test feature creation"""
        # First clean the data
        cleaned_data = self.processor.clean_data(self.sample_data)
        
        # Then create features
        featured_data = self.processor.create_features(cleaned_data)
        
        # Check if new features are created
        expected_features = [
            'year', 'month', 'quarter', 'day_of_week',
            'customer_acceptance_rate', 'customer_avg_discount',
            'lane_acceptance_rate', 'lane_avg_discount',
            'shipment_acceptance_rate', 'shipment_avg_discount'
        ]
        
        for feature in expected_features:
            assert feature in featured_data.columns
    
    def test_get_accepted_quotes_only(self):
        """Test filtering accepted quotes only"""
        self.processor.processed_data = self.sample_data
        accepted_quotes = self.processor.get_accepted_quotes_only()
        
        # All returned quotes should be accepted
        assert all(accepted_quotes['status'] == 'accepted')
        
        # Should return 2 quotes from sample data
        assert len(accepted_quotes) == 2
    
    def test_get_data_summary(self):
        """Test data summary generation"""
        self.processor.processed_data = self.sample_data.copy()
        self.processor.processed_data['date'] = pd.to_datetime(self.processor.processed_data['date'])
        
        summary = self.processor.get_data_summary()
        
        # Check if summary contains expected keys
        expected_keys = [
            'total_records', 'total_customers', 'total_lane_pairs',
            'date_range', 'acceptance_rate', 'shipment_types',
            'commodity_types', 'discount_stats'
        ]
        
        for key in expected_keys:
            assert key in summary
        
        # Check specific values
        assert summary['total_records'] == 3
        assert summary['total_customers'] == 2
        assert summary['acceptance_rate'] == 2/3
