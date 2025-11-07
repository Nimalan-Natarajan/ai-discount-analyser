"""
Tests for static analyzer module
"""
import pytest
import pandas as pd
import numpy as np
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from static_analyzer import StaticAnalyzer

class TestStaticAnalyzer:
    """Test cases for StaticAnalyzer class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.analyzer = StaticAnalyzer()
        
        # Create sample data
        self.sample_data = pd.DataFrame({
            'customer_id': ['CUST001', 'CUST002', 'CUST001', 'CUST002', 'CUST003'],
            'date': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05']),
            'shipment_type': ['air', 'ofr fcl', 'air', 'ofr lcl', 'air'],
            'commodity_type': ['general', 'electronics', 'textiles', 'general', 'electronics'],
            'shipper_country': ['usa', 'china', 'usa', 'china', 'germany'],
            'shipper_station': ['lax', 'sha', 'lax', 'sha', 'ham'],
            'consignee_country': ['germany', 'usa', 'japan', 'germany', 'usa'],
            'consignee_station': ['ham', 'nyc', 'nrt', 'ham', 'lax'],
            'discount_offered': [15.0, 12.0, 18.5, 20.0, 25.0],
            'status': ['accepted', 'rejected', 'accepted', 'accepted', 'rejected'],
            'lane_pair': ['usa_lax-germany_ham', 'china_sha-usa_nyc', 'usa_lax-japan_nrt', 'china_sha-germany_ham', 'germany_ham-usa_lax']
        })
    
    def test_load_data(self):
        """Test loading data for analysis"""
        self.analyzer.load_data(self.sample_data)
        
        assert self.analyzer.data is not None
        assert len(self.analyzer.data) == 5
    
    def test_overall_statistics(self):
        """Test overall statistics calculation"""
        self.analyzer.load_data(self.sample_data)
        stats = self.analyzer.overall_statistics()
        
        # Check basic metrics
        assert stats['total_quotes'] == 5
        assert stats['total_customers'] == 3
        assert stats['overall_acceptance_rate'] == 0.6  # 3 accepted out of 5
        
        # Check discount statistics exist
        assert 'discount_statistics' in stats
        assert 'mean' in stats['discount_statistics']
        assert 'median' in stats['discount_statistics']
    
    def test_customer_analysis(self):
        """Test customer behavior analysis"""
        self.analyzer.load_data(self.sample_data)
        customer_analysis = self.analyzer.customer_analysis()
        
        assert 'total_customers' in customer_analysis
        assert customer_analysis['total_customers'] == 3
        
        # Check for customer categories
        assert 'high_value_customers' in customer_analysis
        assert 'low_value_customers' in customer_analysis
        assert 'most_active_customers' in customer_analysis
    
    def test_lane_analysis(self):
        """Test lane pair performance analysis"""
        self.analyzer.load_data(self.sample_data)
        lane_analysis = self.analyzer.lane_analysis()
        
        assert 'total_lanes' in lane_analysis
        assert lane_analysis['total_lanes'] == 5  # 5 unique lane pairs
        
        # Check for lane performance categories
        assert 'best_performing_lanes' in lane_analysis
        assert 'worst_performing_lanes' in lane_analysis
        assert 'high_volume_lanes' in lane_analysis
    
    def test_shipment_type_analysis(self):
        """Test shipment type performance analysis"""
        self.analyzer.load_data(self.sample_data)
        shipment_analysis = self.analyzer.shipment_type_analysis()
        
        assert 'shipment_type_performance' in shipment_analysis
        
        # Should have data for each shipment type in sample
        performance = shipment_analysis['shipment_type_performance']
        shipment_types = [item['shipment_type'] for item in performance]
        assert 'air' in shipment_types
        assert 'ofr fcl' in shipment_types
        assert 'ofr lcl' in shipment_types
    
    def test_commodity_analysis(self):
        """Test commodity type performance analysis"""
        self.analyzer.load_data(self.sample_data)
        commodity_analysis = self.analyzer.commodity_analysis()
        
        assert 'commodity_performance' in commodity_analysis
        
        # Should have data for each commodity type in sample
        performance = commodity_analysis['commodity_performance']
        commodity_types = [item['commodity_type'] for item in performance]
        assert 'general' in commodity_types
        assert 'electronics' in commodity_types
        assert 'textiles' in commodity_types
    
    def test_temporal_analysis(self):
        """Test temporal trends analysis"""
        self.analyzer.load_data(self.sample_data)
        temporal_analysis = self.analyzer.temporal_analysis()
        
        assert 'monthly_trends' in temporal_analysis
        assert 'quarterly_trends' in temporal_analysis
        assert 'day_of_week_analysis' in temporal_analysis
        assert 'seasonal_patterns' in temporal_analysis
    
    def test_discount_sensitivity_analysis(self):
        """Test discount sensitivity analysis"""
        self.analyzer.load_data(self.sample_data)
        discount_analysis = self.analyzer.discount_sensitivity_analysis()
        
        assert 'discount_bucket_analysis' in discount_analysis
        assert 'discount_acceptance_correlation' in discount_analysis
        assert 'discount_sensitivity_insights' in discount_analysis
        
        # Correlation should be a number between -1 and 1
        correlation = discount_analysis['discount_acceptance_correlation']
        assert -1 <= correlation <= 1
    
    def test_generate_comprehensive_report(self):
        """Test comprehensive report generation"""
        self.analyzer.load_data(self.sample_data)
        report = self.analyzer.generate_comprehensive_report()
        
        # Check all sections are present
        expected_sections = [
            'overall_statistics',
            'customer_analysis',
            'lane_analysis',
            'shipment_type_analysis',
            'commodity_analysis',
            'temporal_analysis',
            'discount_sensitivity_analysis',
            'generated_at'
        ]
        
        for section in expected_sections:
            assert section in report
    
    def test_empty_data_handling(self):
        """Test behavior with empty data"""
        empty_data = pd.DataFrame()
        self.analyzer.load_data(empty_data)
        
        stats = self.analyzer.overall_statistics()
        assert stats == {}
        
        report = self.analyzer.generate_comprehensive_report()
        assert 'error' in report
