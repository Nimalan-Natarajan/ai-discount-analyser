#!/usr/bin/env python3
"""
Show exactly what prompt is sent to Gemini AI with real data from test_quotes.csv
"""
import sys
import os
import pandas as pd

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def show_gemini_prompt_example():
    """Show the exact prompt sent to Gemini AI with real data"""
    print("🤖 **GEMINI AI PROMPT EXAMPLE**")
    print("=" * 60)
    
    try:
        from data_processor import QuoteProcessor
        from ai_predictor import DiscountPredictor
        
        # Load and process the test data
        processor = QuoteProcessor()
        data = processor.load_data("test_quotes.csv")
        
        print(f"📊 Loaded {len(data)} records from test_quotes.csv")
        print(f"✅ Data normalized to internal format")
        
        # Initialize predictor
        predictor = DiscountPredictor()
        predictor.load_historical_data(data)
        
        # Use a real example from the data
        sample_row = data.iloc[0]  # First row: ABC Logistics, AIR, General, India-Mumbai to USA-New York
        
        customer_id = sample_row['customer_id']
        lane_pair = sample_row['lane_pair']  # This will be "india_mumbai-usa_new york"
        shipment_type = sample_row['shipment_type']
        commodity_type = sample_row['commodity_type']
        proposed_discount = 12.5  # Example proposed discount
        
        print(f"\n🎯 **EXAMPLE PREDICTION REQUEST:**")
        print(f"   Customer: {customer_id}")
        print(f"   Lane: {lane_pair}")
        print(f"   Shipment Type: {shipment_type}")
        print(f"   Commodity: {commodity_type}")
        print(f"   Proposed Discount: {proposed_discount}%")
        
        # Build the context that gets sent to Gemini
        context = predictor._build_context(customer_id, lane_pair, shipment_type, commodity_type)
        
        # Get normalized inputs
        norm_inputs = predictor._normalize_inputs(customer_id, lane_pair, shipment_type, commodity_type)
        norm_shipment_type, norm_lane_pair, norm_customer_id, norm_commodity_type = norm_inputs
        
        print(f"\n" + "="*80)
        print(f"📝 **COMPLETE PROMPT SENT TO GEMINI AI:**")
        print(f"="*80)
        
        # This is the EXACT prompt structure sent to Gemini
        full_prompt = f"""You are an AI logistics expert analyzing discount acceptance for quotes.
Based on historical data patterns, predict the likelihood of quote acceptance.

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
- Market conditions"""

        print(full_prompt)
        
        print(f"\n" + "="*80)
        print(f"🧠 **WHAT GEMINI AI RECEIVES:**")
        print(f"="*80)
        print(f"1. 📊 **Rich Historical Context** - Customer, lane, shipment, commodity analytics")
        print(f"2. 🎯 **Current Quote Details** - Specific quote to predict")
        print(f"3. 📋 **Structured Output Request** - JSON format for consistent responses")
        print(f"4. 💡 **Analysis Guidelines** - Factors to consider in prediction")
        
        print(f"\n🔍 **KEY DATA GEMINI ANALYZES:**")
        
        # Show some specific analytics that go to Gemini
        customer_data = data[data['customer_id'] == customer_id]
        lane_data = data[data['lane_pair'] == lane_pair]
        shipment_data = data[data['shipment_type'] == shipment_type]
        commodity_data = data[data['commodity_type'] == commodity_type]
        
        print(f"   📈 Customer '{customer_id}': {len(customer_data)} quotes, {(customer_data['status'] == 'accepted').mean():.1%} acceptance")
        print(f"   🛣️  Lane '{lane_pair}': {len(lane_data)} quotes, {(lane_data['status'] == 'accepted').mean():.1%} acceptance")
        print(f"   📦 Shipment '{shipment_type}': {len(shipment_data)} quotes, {(shipment_data['status'] == 'accepted').mean():.1%} acceptance")
        print(f"   📋 Commodity '{commodity_type}': {len(commodity_data)} quotes, {(commodity_data['status'] == 'accepted').mean():.1%} acceptance")
        
        print(f"\n💰 **DISCOUNT INSIGHTS:**")
        accepted_data = data[data['status'] == 'accepted']
        print(f"   • Average accepted discount: {accepted_data['discount_offered'].mean():.1f}%")
        print(f"   • Max accepted discount: {accepted_data['discount_offered'].max():.1f}%")
        print(f"   • Min accepted discount: {accepted_data['discount_offered'].min():.1f}%")
        
        print(f"\n🤖 **GEMINI AI THEN RETURNS:**")
        print(f"```json")
        print(f"{{")
        print(f'    "acceptance_probability": 0.75,')
        print(f'    "confidence_level": 0.82,')
        print(f'    "key_factors": [')
        print(f'        "Customer has 85% historical acceptance rate",')
        print(f'        "This lane shows strong performance",')
        print(f'        "AIR shipments typically accepted at this discount level"')
        print(f'    ],')
        print(f'    "recommended_discount": 11.2,')
        print(f'    "reasoning": "Based on historical patterns...",')
        print(f'    "risk_assessment": "low"')
        print(f"}} ")
        print(f"```")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 Analyzing Gemini AI prompt structure with your test_quotes.csv data...\n")
    
    success = show_gemini_prompt_example()
    
    if success:
        print(f"\n🎉 **SUMMARY:**")
        print(f"✅ Gemini receives rich contextual data about customer, lane, shipment patterns")
        print(f"🧠 AI analyzes historical trends to predict quote acceptance")
        print(f"📊 Returns structured JSON with probability, confidence, and reasoning")
        print(f"💡 This enables intelligent discount recommendations!")
    else:
        print(f"\n💔 Could not generate example - check if test_quotes.csv is accessible")
