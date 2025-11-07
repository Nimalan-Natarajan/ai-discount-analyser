"""
Utility helper functions for the Logistics Quotation Management Tool
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import logging

def setup_logging(level: str = 'INFO') -> logging.Logger:
    """Setup logging configuration"""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def validate_quote_data(data: Dict[str, Any]) -> bool:
    """Validate quote data structure"""
    required_fields = [
        'customer_id', 'date', 'shipment_type', 'commodity_type',
        'shipper_country', 'shipper_station', 'consignee_country',
        'consignee_station', 'discount_offered', 'status'
    ]
    
    return all(field in data for field in required_fields)

def create_lane_pair(shipper_country: str, shipper_station: str,
                    consignee_country: str, consignee_station: str) -> str:
    """Create a standardized lane pair identifier"""
    return f"{shipper_country}_{shipper_station}-{consignee_country}_{consignee_station}"

def calculate_acceptance_rate(df: pd.DataFrame, group_by: List[str]) -> pd.DataFrame:
    """Calculate acceptance rates grouped by specified columns"""
    if df.empty:
        return pd.DataFrame()
    
    grouped = df.groupby(group_by).agg({
        'status': ['count', lambda x: (x == 'accepted').sum()]
    }).round(3)
    
    grouped.columns = ['total_quotes', 'accepted_quotes']
    grouped['acceptance_rate'] = (grouped['accepted_quotes'] / grouped['total_quotes']).round(3)
    
    return grouped.reset_index()

def filter_accepted_quotes(df: pd.DataFrame) -> pd.DataFrame:
    """Filter dataframe to include only accepted quotes"""
    return df[df['status'] == 'accepted'].copy()

def get_customer_history(df: pd.DataFrame, customer_id: str) -> Dict[str, Any]:
    """Get customer's historical quote data and statistics"""
    customer_data = df[df['customer_id'] == customer_id].copy()
    
    if customer_data.empty:
        return {}
    
    total_quotes = len(customer_data)
    accepted_quotes = len(customer_data[customer_data['status'] == 'accepted'])
    acceptance_rate = accepted_quotes / total_quotes if total_quotes > 0 else 0
    
    avg_discount_accepted = customer_data[
        customer_data['status'] == 'accepted'
    ]['discount_offered'].mean()
    
    return {
        'total_quotes': total_quotes,
        'accepted_quotes': accepted_quotes,
        'acceptance_rate': round(acceptance_rate, 3),
        'average_accepted_discount': round(avg_discount_accepted, 3) if not pd.isna(avg_discount_accepted) else 0,
        'preferred_shipment_types': customer_data['shipment_type'].value_counts().to_dict(),
        'preferred_commodity_types': customer_data['commodity_type'].value_counts().to_dict()
    }

def encode_categorical_features(df: pd.DataFrame, categorical_columns: List[str]) -> pd.DataFrame:
    """Encode categorical features for machine learning"""
    df_encoded = df.copy()
    
    for col in categorical_columns:
        if col in df_encoded.columns:
            df_encoded = pd.get_dummies(df_encoded, columns=[col], prefix=col)
    
    return df_encoded

def format_currency(amount: float, currency: str = 'USD') -> str:
    """Format currency amounts"""
    return f"{currency} {amount:,.2f}"

def validate_discount_range(discount: float) -> bool:
    """Validate if discount is within acceptable range (0-100%)"""
    return 0 <= discount <= 100
