"""
Data processing module for logistics quotation data
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
import logging

try:
    from .utils.helpers import (
        setup_logging, validate_quote_data, create_lane_pair,
        filter_accepted_quotes, get_customer_history
    )
    from .utils.config import Config
except ImportError:
    # Fallback for direct execution
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from utils.helpers import (
        setup_logging, validate_quote_data, create_lane_pair,
        filter_accepted_quotes, get_customer_history
    )
    from utils.config import Config

class QuoteProcessor:
    """Handle data processing for logistics quotes"""
    
    def __init__(self):
        self.logger = setup_logging(Config.LOG_LEVEL)
    
    def normalize_data_format(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convert test_quotes.csv format to internal format"""
        try:
            # Check if we have the test format columns
            test_format_columns = [
                'date', 'customerName', 'shipmentType', 'commodityType',
                'shipperCountry', 'shipperStation', 'consigneeCountry',
                'consigneeStation', 'discount', 'accepted'
            ]
            
            if all(col in df.columns for col in test_format_columns):
                self.logger.info("Converting test_quotes.csv format to internal format")
                
                # Create a copy to avoid modifying original
                normalized_df = df.copy()
                
                # Column mappings
                column_mapping = {
                    'customerName': 'customer_id',
                    'shipmentType': 'shipment_type',
                    'commodityType': 'commodity_type',
                    'shipperCountry': 'shipper_country',
                    'shipperStation': 'shipper_station',
                    'consigneeCountry': 'consignee_country',
                    'consigneeStation': 'consignee_station',
                    'discount': 'discount_offered'
                }
                
                # Rename columns
                normalized_df = normalized_df.rename(columns=column_mapping)
                
                # Convert accepted (TRUE/FALSE) to status (accepted/rejected)
                if 'accepted' in normalized_df.columns:
                    normalized_df['status'] = normalized_df['accepted'].apply(
                        lambda x: 'accepted' if str(x).upper() in ['TRUE', 'T', '1', 'YES'] else 'rejected'
                    )
                    normalized_df = normalized_df.drop('accepted', axis=1)
                
                # Ensure date format consistency (convert M/D/YYYY to YYYY-MM-DD)
                if 'date' in normalized_df.columns:
                    try:
                        normalized_df['date'] = pd.to_datetime(normalized_df['date']).dt.strftime('%Y-%m-%d')
                    except Exception as e:
                        self.logger.warning(f"Could not convert date format: {e}")
                
                self.logger.info(f"Successfully normalized {len(normalized_df)} rows from test format")
                return normalized_df
            else:
                # Already in internal format or different format
                self.logger.info("Data already in internal format or different format detected")
                return df
                
        except Exception as e:
            self.logger.error(f"Error normalizing data format: {e}")
            return df
        self.data = None
        self.processed_data = None
        
    def load_data(self, file_path: str) -> pd.DataFrame:
        """Load quote data from CSV file"""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"Data file not found: {file_path}")
            
            # Load raw data
            raw_data = pd.read_csv(file_path)
            self.logger.info(f"Loaded {len(raw_data)} records from {file_path}")
            
            # Normalize format (converts test_quotes.csv format if needed)
            self.data = self.normalize_data_format(raw_data)
            
            return self.data
            
        except Exception as e:
            self.logger.error(f"Error loading data: {str(e)}")
            raise
    
    def validate_data(self, df: pd.DataFrame) -> bool:
        """Validate the structure and content of quote data (expects normalized internal format)"""
        try:
            # After normalization, we should always have the internal format
            required_columns = [
                'customer_id', 'date', 'shipment_type', 'commodity_type',
                'shipper_country', 'shipper_station', 'consignee_country',
                'consignee_station', 'discount_offered', 'status'
            ]
            
            # Check for required columns
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                self.logger.error(f"Missing required columns after normalization: {missing_columns}")
                return False
            
            self.logger.info(f"Validating data with {len(df)} records and columns: {list(df.columns)}")
            
            # Check for required columns
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                self.logger.error(f"Missing required columns: {missing_columns}")
                return False
            
            # Check for empty dataframe
            if df.empty:
                self.logger.error("Dataframe is empty")
                return False
            
            # Check for null values in critical columns (normalized format)
            critical_cols = ['customer_id', 'status']
            critical_nulls = df[critical_cols].isnull().sum()
            if critical_nulls.any():
                self.logger.error(f"Null values found in critical columns: {critical_nulls[critical_nulls > 0].to_dict()}")
                return False
            
            # Check discount range (allow NaN values, they'll be handled later)
            discount_col = 'discount_offered'
            valid_discounts = df[discount_col].notna()
            if valid_discounts.any():
                discount_data = df[valid_discounts][discount_col]
                invalid_discounts = discount_data[(discount_data < 0) | (discount_data > 100)]
                if len(invalid_discounts) > 0:
                    self.logger.warning(f"Found {len(invalid_discounts)} records with invalid discount ranges (will be cleaned)")
            
            # Check status values (normalized format uses accepted/rejected)
            valid_statuses = ['accepted', 'rejected']
            status_col = 'status'
            invalid_statuses = df[~df[status_col].str.lower().isin([s.lower() for s in valid_statuses])]
            if not invalid_statuses.empty:
                self.logger.warning(f"Found {len(invalid_statuses)} records with invalid status values (will be cleaned)")
                unique_statuses = df[status_col].unique()
                self.logger.info(f"Found status values: {unique_statuses}")
            
            self.logger.info("Data validation completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error during validation: {str(e)}")
            return False
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize the data"""
        df_clean = df.copy()
        
        # Convert date column to datetime
        df_clean['date'] = pd.to_datetime(df_clean['date'], errors='coerce')
        
        # Standardize text columns
        text_columns = ['shipment_type', 'commodity_type', 'status',
                       'shipper_country', 'shipper_station',
                       'consignee_country', 'consignee_station']
        
        for col in text_columns:
            if col in df_clean.columns:
                df_clean[col] = df_clean[col].astype(str).str.strip().str.lower()
        
        # Create lane pair identifier
        df_clean['lane_pair'] = df_clean.apply(
            lambda row: create_lane_pair(
                row['shipper_country'], row['shipper_station'],
                row['consignee_country'], row['consignee_station']
            ), axis=1
        )
        
        # Remove duplicates
        initial_count = len(df_clean)
        df_clean = df_clean.drop_duplicates()
        removed_duplicates = initial_count - len(df_clean)
        
        if removed_duplicates > 0:
            self.logger.info(f"Removed {removed_duplicates} duplicate records")
        
        # Handle missing values
        df_clean = df_clean.dropna(subset=['customer_id', 'date', 'discount_offered', 'status'])
        
        # Filter valid discount ranges
        df_clean = df_clean[
            (df_clean['discount_offered'] >= 0) & (df_clean['discount_offered'] <= 100)
        ]
        
        # Filter valid status values
        df_clean = df_clean[df_clean['status'].isin(['accepted', 'rejected'])]
        
        self.logger.info(f"Data cleaned. Final dataset: {len(df_clean)} records")
        
        return df_clean
    
    def create_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create additional features for analysis and modeling"""
        df_features = df.copy()
        
        # Date-based features
        df_features['year'] = df_features['date'].dt.year
        df_features['month'] = df_features['date'].dt.month
        df_features['quarter'] = df_features['date'].dt.quarter
        df_features['day_of_week'] = df_features['date'].dt.dayofweek
        
        # Customer-based features
        customer_stats = df_features.groupby('customer_id').agg({
            'status': lambda x: (x == 'accepted').mean(),
            'discount_offered': 'mean'
        }).round(3)
        
        customer_stats.columns = ['customer_acceptance_rate', 'customer_avg_discount']
        df_features = df_features.merge(
            customer_stats, left_on='customer_id', right_index=True, how='left'
        )
        
        # Lane-based features
        lane_stats = df_features.groupby('lane_pair').agg({
            'status': lambda x: (x == 'accepted').mean(),
            'discount_offered': 'mean'
        }).round(3)
        
        lane_stats.columns = ['lane_acceptance_rate', 'lane_avg_discount']
        df_features = df_features.merge(
            lane_stats, left_on='lane_pair', right_index=True, how='left'
        )
        
        # Shipment type features
        shipment_stats = df_features.groupby('shipment_type').agg({
            'status': lambda x: (x == 'accepted').mean(),
            'discount_offered': 'mean'
        }).round(3)
        
        shipment_stats.columns = ['shipment_acceptance_rate', 'shipment_avg_discount']
        df_features = df_features.merge(
            shipment_stats, left_on='shipment_type', right_index=True, how='left'
        )
        
        self.logger.info("Feature engineering completed")
        
        return df_features
    
    def process_data(self, file_path: str) -> pd.DataFrame:
        """Complete data processing pipeline"""
        # Load data (includes normalization from test_quotes.csv format)
        normalized_data = self.load_data(file_path)
        
        # Validate normalized data (now in internal format)
        if not self.validate_data(normalized_data):
            raise ValueError("Data validation failed")
        
        # Clean data
        cleaned_data = self.clean_data(normalized_data)
        
        # Create features
        processed_data = self.create_features(cleaned_data)
        
        self.processed_data = processed_data
        return processed_data
    
    def get_accepted_quotes_only(self) -> pd.DataFrame:
        """Return only accepted quotes for training purposes"""
        if self.processed_data is None:
            raise ValueError("No processed data available. Run process_data() first.")
        
        return filter_accepted_quotes(self.processed_data)
    
    def save_processed_data(self, output_path: str) -> None:
        """Save processed data to CSV"""
        if self.processed_data is None:
            raise ValueError("No processed data to save")
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.processed_data.to_csv(output_path, index=False)
        self.logger.info(f"Processed data saved to {output_path}")
    
    def get_data_summary(self) -> Dict:
        """Get summary statistics of the processed data"""
        if self.processed_data is None:
            return {}
        
        df = self.processed_data
        
        # Check if lane_pair column exists (processed data) or needs to be created on the fly
        if 'lane_pair' in df.columns:
            total_lane_pairs = df['lane_pair'].nunique()
        else:
            # Create lane_pair on the fly for raw data
            temp_lane_pairs = df.apply(
                lambda row: f"{row['shipper_country']}-{row['shipper_station']} to {row['consignee_country']}-{row['consignee_station']}", 
                axis=1
            )
            total_lane_pairs = temp_lane_pairs.nunique()
        
        return {
            'total_records': len(df),
            'total_customers': df['customer_id'].nunique(),
            'total_lane_pairs': total_lane_pairs,
            'date_range': {
                'start': df['date'].min().strftime('%Y-%m-%d'),
                'end': df['date'].max().strftime('%Y-%m-%d')
            },
            'acceptance_rate': round((df['status'] == 'accepted').mean(), 3),
            'shipment_types': df['shipment_type'].value_counts().to_dict(),
            'commodity_types': df['commodity_type'].value_counts().to_dict(),
            'discount_stats': {
                'mean': round(df['discount_offered'].mean(), 2),
                'median': round(df['discount_offered'].median(), 2),
                'std': round(df['discount_offered'].std(), 2),
                'min': round(df['discount_offered'].min(), 2),
                'max': round(df['discount_offered'].max(), 2)
            }
        }
