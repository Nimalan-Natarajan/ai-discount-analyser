"""
Static analysis module for logistics quotation data
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import logging
from collections import defaultdict

try:
    from .utils.helpers import (
        setup_logging, calculate_acceptance_rate, 
        filter_accepted_quotes, get_customer_history
    )
    from .utils.config import Config
except ImportError:
    # Fallback for direct execution
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from utils.helpers import (
        setup_logging, calculate_acceptance_rate, 
        filter_accepted_quotes, get_customer_history
    )
    from utils.config import Config

class StaticAnalyzer:
    """Statistical analysis of logistics quotation data"""
    
    def __init__(self):
        self.logger = setup_logging(Config.LOG_LEVEL)
        self.data = None
    
    def load_data(self, df: pd.DataFrame) -> None:
        """Load data for analysis"""
        self.data = df.copy()
        self.logger.info(f"Loaded {len(df)} records for static analysis")
    
    def overall_statistics(self) -> Dict[str, Any]:
        """Calculate overall dataset statistics"""
        if self.data is None:
            return {}
        
        df = self.data
        accepted_df = filter_accepted_quotes(df)
        
        return {
            'total_quotes': len(df),
            'total_customers': df['customer_id'].nunique(),
            'total_lane_pairs': df['lane_pair'].nunique(),
            'overall_acceptance_rate': round((df['status'] == 'accepted').mean(), 3),
            'total_accepted_quotes': len(accepted_df),
            'date_range': {
                'start': df['date'].min().strftime('%Y-%m-%d'),
                'end': df['date'].max().strftime('%Y-%m-%d'),
                'span_days': (df['date'].max() - df['date'].min()).days
            },
            'discount_statistics': {
                'mean': round(df['discount_offered'].mean(), 2),
                'median': round(df['discount_offered'].median(), 2),
                'std': round(df['discount_offered'].std(), 2),
                'min': round(df['discount_offered'].min(), 2),
                'max': round(df['discount_offered'].max(), 2),
                'quartiles': {
                    'q25': round(df['discount_offered'].quantile(0.25), 2),
                    'q75': round(df['discount_offered'].quantile(0.75), 2)
                }
            },
            'accepted_discount_statistics': {
                'mean': round(accepted_df['discount_offered'].mean(), 2),
                'median': round(accepted_df['discount_offered'].median(), 2),
                'std': round(accepted_df['discount_offered'].std(), 2),
                'min': round(accepted_df['discount_offered'].min(), 2),
                'max': round(accepted_df['discount_offered'].max(), 2)
            } if not accepted_df.empty else {}
        }
    
    def customer_analysis(self) -> Dict[str, Any]:
        """Analyze customer behavior patterns"""
        if self.data is None:
            return {}
        
        df = self.data
        customer_stats = []
        
        for customer_id in df['customer_id'].unique():
            customer_data = get_customer_history(df, customer_id)
            customer_stats.append({
                'customer_id': customer_id,
                **customer_data
            })
        
        customer_df = pd.DataFrame(customer_stats)
        
        return {
            'total_customers': len(customer_df),
            'customer_acceptance_rates': {
                'mean': round(customer_df['acceptance_rate'].mean(), 3),
                'median': round(customer_df['acceptance_rate'].median(), 3),
                'std': round(customer_df['acceptance_rate'].std(), 3),
                'min': round(customer_df['acceptance_rate'].min(), 3),
                'max': round(customer_df['acceptance_rate'].max(), 3)
            },
            'high_value_customers': customer_df[
                customer_df['acceptance_rate'] > 0.7
            ]['customer_id'].tolist(),
            'low_value_customers': customer_df[
                customer_df['acceptance_rate'] < 0.3
            ]['customer_id'].tolist(),
            'most_active_customers': customer_df.nlargest(10, 'total_quotes')[
                ['customer_id', 'total_quotes', 'acceptance_rate']
            ].to_dict('records')
        }
    
    def lane_analysis(self) -> Dict[str, Any]:
        """Analyze lane pair performance"""
        if self.data is None:
            return {}
        
        df = self.data
        lane_stats = calculate_acceptance_rate(df, ['lane_pair'])
        
        # Get additional lane metrics
        lane_discount_stats = df.groupby('lane_pair').agg({
            'discount_offered': ['mean', 'median', 'std', 'min', 'max']
        }).round(2)
        
        lane_discount_stats.columns = ['avg_discount', 'median_discount', 
                                     'std_discount', 'min_discount', 'max_discount']
        
        lane_combined = lane_stats.merge(
            lane_discount_stats, left_on='lane_pair', right_index=True
        )
        
        return {
            'total_lanes': len(lane_stats),
            'best_performing_lanes': lane_combined.nlargest(10, 'acceptance_rate')[
                ['lane_pair', 'acceptance_rate', 'total_quotes', 'avg_discount']
            ].to_dict('records'),
            'worst_performing_lanes': lane_combined.nsmallest(10, 'acceptance_rate')[
                ['lane_pair', 'acceptance_rate', 'total_quotes', 'avg_discount']
            ].to_dict('records'),
            'high_volume_lanes': lane_combined.nlargest(10, 'total_quotes')[
                ['lane_pair', 'total_quotes', 'acceptance_rate', 'avg_discount']
            ].to_dict('records'),
            'lane_acceptance_distribution': {
                'high_acceptance_lanes': len(lane_stats[lane_stats['acceptance_rate'] > 0.7]),
                'medium_acceptance_lanes': len(lane_stats[
                    (lane_stats['acceptance_rate'] >= 0.3) & 
                    (lane_stats['acceptance_rate'] <= 0.7)
                ]),
                'low_acceptance_lanes': len(lane_stats[lane_stats['acceptance_rate'] < 0.3])
            }
        }
    
    def shipment_type_analysis(self) -> Dict[str, Any]:
        """Analyze performance by shipment type"""
        if self.data is None:
            return {}
        
        df = self.data
        shipment_stats = calculate_acceptance_rate(df, ['shipment_type'])
        
        # Get discount statistics by shipment type
        shipment_discount_stats = df.groupby('shipment_type').agg({
            'discount_offered': ['mean', 'median', 'std']
        }).round(2)
        
        shipment_discount_stats.columns = ['avg_discount', 'median_discount', 'std_discount']
        
        shipment_combined = shipment_stats.merge(
            shipment_discount_stats, left_on='shipment_type', right_index=True
        )
        
        return {
            'shipment_type_performance': shipment_combined.to_dict('records'),
            'best_shipment_type': shipment_combined.loc[
                shipment_combined['acceptance_rate'].idxmax()
            ].to_dict() if not shipment_combined.empty else {},
            'most_popular_shipment_type': shipment_combined.loc[
                shipment_combined['total_quotes'].idxmax()
            ].to_dict() if not shipment_combined.empty else {}
        }
    
    def commodity_analysis(self) -> Dict[str, Any]:
        """Analyze performance by commodity type"""
        if self.data is None:
            return {}
        
        df = self.data
        commodity_stats = calculate_acceptance_rate(df, ['commodity_type'])
        
        # Get discount statistics by commodity type
        commodity_discount_stats = df.groupby('commodity_type').agg({
            'discount_offered': ['mean', 'median', 'std']
        }).round(2)
        
        commodity_discount_stats.columns = ['avg_discount', 'median_discount', 'std_discount']
        
        commodity_combined = commodity_stats.merge(
            commodity_discount_stats, left_on='commodity_type', right_index=True
        )
        
        return {
            'commodity_performance': commodity_combined.to_dict('records'),
            'best_commodity_type': commodity_combined.loc[
                commodity_combined['acceptance_rate'].idxmax()
            ].to_dict() if not commodity_combined.empty else {},
            'most_popular_commodity': commodity_combined.loc[
                commodity_combined['total_quotes'].idxmax()
            ].to_dict() if not commodity_combined.empty else {}
        }
    
    def temporal_analysis(self) -> Dict[str, Any]:
        """Analyze trends over time"""
        if self.data is None:
            return {}
        
        df = self.data.copy()
        df['year_month'] = df['date'].dt.to_period('M')
        
        # Monthly trends
        monthly_stats = calculate_acceptance_rate(df, ['year_month'])
        monthly_stats['year_month'] = monthly_stats['year_month'].astype(str)
        
        # Quarterly trends
        df['quarter'] = df['date'].dt.to_period('Q')
        quarterly_stats = calculate_acceptance_rate(df, ['quarter'])
        quarterly_stats['quarter'] = quarterly_stats['quarter'].astype(str)
        
        # Day of week analysis
        df['day_of_week'] = df['date'].dt.day_name()
        dow_stats = calculate_acceptance_rate(df, ['day_of_week'])
        
        return {
            'monthly_trends': monthly_stats.to_dict('records'),
            'quarterly_trends': quarterly_stats.to_dict('records'),
            'day_of_week_analysis': dow_stats.to_dict('records'),
            'seasonal_patterns': {
                'best_month': monthly_stats.loc[
                    monthly_stats['acceptance_rate'].idxmax()
                ]['year_month'] if not monthly_stats.empty else None,
                'worst_month': monthly_stats.loc[
                    monthly_stats['acceptance_rate'].idxmin()
                ]['year_month'] if not monthly_stats.empty else None,
                'best_quarter': quarterly_stats.loc[
                    quarterly_stats['acceptance_rate'].idxmax()
                ]['quarter'] if not quarterly_stats.empty else None,
                'best_day_of_week': dow_stats.loc[
                    dow_stats['acceptance_rate'].idxmax()
                ]['day_of_week'] if not dow_stats.empty else None
            }
        }
    
    def discount_sensitivity_analysis(self) -> Dict[str, Any]:
        """Analyze relationship between discount levels and acceptance rates"""
        if self.data is None:
            return {}
        
        df = self.data
        
        # Create discount buckets
        df_analysis = df.copy()
        df_analysis['discount_bucket'] = pd.cut(
            df_analysis['discount_offered'],
            bins=[0, 5, 10, 15, 20, 25, 30, 100],
            labels=['0-5%', '5-10%', '10-15%', '15-20%', '20-25%', '25-30%', '30%+']
        )
        
        bucket_stats = calculate_acceptance_rate(df_analysis, ['discount_bucket'])
        
        # Calculate correlation between discount and acceptance
        correlation = df['discount_offered'].corr(
            (df['status'] == 'accepted').astype(int)
        )
        
        return {
            'discount_bucket_analysis': bucket_stats.to_dict('records'),
            'discount_acceptance_correlation': round(correlation, 3),
            'optimal_discount_range': self._find_optimal_discount_range(df),
            'discount_sensitivity_insights': self._generate_discount_insights(bucket_stats)
        }
    
    def _find_optimal_discount_range(self, df: pd.DataFrame) -> Dict[str, float]:
        """Find the discount range with highest acceptance rates"""
        # Create more granular buckets for analysis
        df_analysis = df.copy()
        df_analysis['discount_bucket'] = pd.cut(
            df_analysis['discount_offered'],
            bins=20,  # 20 buckets for more granular analysis
            precision=1
        )
        
        bucket_stats = calculate_acceptance_rate(df_analysis, ['discount_bucket'])
        
        if bucket_stats.empty:
            return {}
        
        best_bucket = bucket_stats.loc[bucket_stats['acceptance_rate'].idxmax()]
        
        return {
            'optimal_range': str(best_bucket['discount_bucket']),
            'acceptance_rate': best_bucket['acceptance_rate'],
            'sample_size': best_bucket['total_quotes']
        }
    
    def _generate_discount_insights(self, bucket_stats: pd.DataFrame) -> List[str]:
        """Generate insights from discount bucket analysis"""
        insights = []
        
        if bucket_stats.empty:
            return insights
        
        # Find best performing bucket
        best_bucket = bucket_stats.loc[bucket_stats['acceptance_rate'].idxmax()]
        insights.append(f"Highest acceptance rate ({best_bucket['acceptance_rate']:.1%}) in {best_bucket['discount_bucket']} range")
        
        # Find patterns
        high_acceptance_buckets = bucket_stats[bucket_stats['acceptance_rate'] > 0.6]
        if not high_acceptance_buckets.empty:
            insights.append(f"{len(high_acceptance_buckets)} discount ranges show high acceptance rates (>60%)")
        
        # Volume vs acceptance trade-off
        high_volume_bucket = bucket_stats.loc[bucket_stats['total_quotes'].idxmax()]
        if high_volume_bucket.name != best_bucket.name:
            insights.append(f"Most popular discount range ({high_volume_bucket['discount_bucket']}) has {high_volume_bucket['acceptance_rate']:.1%} acceptance rate")
        
        return insights
    
    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """Generate a comprehensive analysis report"""
        if self.data is None:
            return {'error': 'No data loaded for analysis'}
        
        return {
            'overall_statistics': self.overall_statistics(),
            'customer_analysis': self.customer_analysis(),
            'lane_analysis': self.lane_analysis(),
            'shipment_type_analysis': self.shipment_type_analysis(),
            'commodity_analysis': self.commodity_analysis(),
            'temporal_analysis': self.temporal_analysis(),
            'discount_sensitivity_analysis': self.discount_sensitivity_analysis(),
            'generated_at': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
        }
