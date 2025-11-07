# Replacement function for quote_optimizer_page
def quote_optimizer_page():
    """Static predictions page"""
    st.header("📊 Static Predictions")
    
    if not st.session_state.data_loaded:
        st.warning("⚠️ Please upload data first in the 'Data Upload' section.")
        return
    
    st.markdown("Analyze historical data patterns to predict optimal discount ranges for maximum acceptance probability.")
    
    df = st.session_state.processed_data
    
    # Input form
    col1, col2 = st.columns(2)
    
    with col1:
        customer_id = st.selectbox(
            "Customer ID",
            options=sorted(df['customer_id'].unique()),
            key="optimizer_customer"
        )
        
        shipment_type = st.selectbox(
            "Shipment Type",
            options=Config.SHIPMENT_TYPES,
            key="optimizer_shipment"
        )
    
    with col2:
        commodity_type = st.selectbox(
            "Commodity Type",
            options=Config.COMMODITY_TYPES,
            key="optimizer_commodity"
        )
        
        lane_pair = st.selectbox(
            "Lane Pair",
            options=sorted(df['lane_pair'].unique()),
            key="optimizer_lane"
        )
    
    # Discount range
    st.subheader("Discount Range to Test")
    col1, col2 = st.columns(2)
    with col1:
        min_discount = st.number_input("Minimum Discount (%)", value=0.0, min_value=0.0, max_value=50.0)
    with col2:
        max_discount = st.number_input("Maximum Discount (%)", value=30.0, min_value=0.0, max_value=50.0)
    
    # Historical data analysis section
    st.markdown("This analysis uses only historical data to find optimal discount patterns.")
    
    if st.button("📊 Analyze Historical Data", type="primary"):
        with st.spinner("Analyzing historical data..."):
            optimization = st.session_state.predictor.get_static_discount_analysis(
                customer_id=customer_id,
                lane_pair=lane_pair,
                shipment_type=shipment_type.lower(),
                commodity_type=commodity_type,
                discount_range=(min_discount, max_discount)
            )
        
        if 'error' not in optimization:
            st.success("✅ Historical Analysis Complete!")
            display_optimization_results(optimization, is_static=True)
        else:
            st.error(f"Analysis failed: {optimization['error']}")
    
    # Help section
    st.markdown("---")
    st.subheader("💡 How It Works")
    
    st.info("""
    **📊 Historical Data Analysis**
    - ⚡ Very fast (< 2 seconds)
    - Uses only your uploaded historical data
    - Analyzes similar past quotes to find patterns
    - Provides optimal discount recommendations based on acceptance rates
    - No external API calls required
    
    **Key Features:**
    - Analyzes customer-specific patterns
    - Lane-based pricing trends
    - Shipment and commodity type preferences
    - Statistical confidence scoring
    """)
