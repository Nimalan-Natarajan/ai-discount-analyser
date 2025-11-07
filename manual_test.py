#!/usr/bin/env python3
"""
Simple validation test to check if our format conversion works
"""
import pandas as pd

# Test data in the new format
test_data = {
    'date': ['1/1/2025', '1/2/2025'],
    'customerName': ['ABC Logistics', 'XYZ Freight'],
    'shipmentType': ['AIR', 'OFR FCL'],
    'commodityType': ['General', 'Temperature Controlled'],
    'shipperCountry': ['India', 'India'],
    'shipperStation': ['Mumbai', 'Mumbai'],
    'consigneeCountry': ['USA', 'Singapore'],
    'consigneeStation': ['New York', 'Singapore'],
    'discount': [10, 8],
    'accepted': [True, True]
}

test_df = pd.DataFrame(test_data)
print("Test dataframe created:")
print(test_df)
print("\nColumns:", list(test_df.columns))

# Test conversion logic manually
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

normalized_df = test_df.rename(columns=column_mapping)
normalized_df['status'] = normalized_df['accepted'].apply(
    lambda x: 'accepted' if str(x).upper() in ['TRUE', 'T', '1', 'YES'] else 'rejected'
)
normalized_df = normalized_df.drop('accepted', axis=1)

print("\nNormalized dataframe:")
print(normalized_df)
print("\nNormalized columns:", list(normalized_df.columns))
