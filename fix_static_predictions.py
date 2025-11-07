#!/usr/bin/env python3
"""
Script to fix the Static Predictions page by removing AI-powered analysis
"""

def fix_static_predictions():
    """Remove AI-powered analysis from Static Predictions page"""
    
    # Read the file
    with open('src/app.py', 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    # Find and replace the analysis section
    old_section = '''    # Static analysis section
    st.markdown("This analysis uses only historical data to find optimal discount patterns.")
    
    with col1:
        if st.button("📊 Quick Static Analysis", type="secondary"):
            with st.spinner("Analyzing historical data..."):
                optimization = st.session_state.predictor.get_static_discount_analysis(
                    customer_id=customer_id,
                    lane_pair=lane_pair,
                    shipment_type=shipment_type.lower(),
                    commodity_type=commodity_type,
                    discount_range=(min_discount, max_discount)
                )
            
            if 'error' not in optimization:
                st.success("✅ Static Analysis Complete!")
                display_optimization_results(optimization, is_static=True)
            else:
                st.error(f"Analysis failed: {optimization['error']}")
    
    with col2:
        if st.button("🤖 AI-Powered Analysis", type="primary"):
            current_api_key = st.session_state.get('gemini_api_key', '') or os.getenv('GEMINI_API_KEY', '')
            if current_api_key:
                with st.spinner("AI analyzing discount range... (this may take 30-60 seconds)"):
                    optimization = st.session_state.predictor.get_optimal_discount_suggestions(
                        customer_id=customer_id,
                        lane_pair=lane_pair,
                        shipment_type=shipment_type.lower(),
                        commodity_type=commodity_type,
                        discount_range=(min_discount, max_discount)
                    )
            
                if 'error' not in optimization:
                    st.success("✅ AI Analysis Complete!")
                    display_optimization_results(optimization, is_static=False)
                else:
                    st.error(f"AI Analysis failed: {optimization['error']}")
            else:
                st.error("🔑 Gemini API key required for AI analysis. Please configure it in Settings.")'''

    new_section = '''    # Historical data analysis section
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
            st.error(f"Analysis failed: {optimization['error']}")'''
    
    # First try direct replacement
    if old_section in content:
        content = content.replace(old_section, new_section)
        print("✅ Direct replacement successful")
    else:
        print("❌ Direct replacement failed, trying character replacement...")
        
        # Try replacing with different emoji encodings
        variations = [
            'st.button("📊 Quick Static Analysis"',
            'st.button("� Quick Static Analysis"',  # Possible encoding issue
            'Quick Static Analysis'
        ]
        
        found = False
        for variation in variations:
            if variation in content:
                print(f"✅ Found variation: {variation}")
                found = True
                break
        
        if not found:
            print("❌ Could not find the section to replace")
            return False
    
    # Also update the help section to remove AI explanation
    old_help = '''    # Help section
    st.markdown("---")
    st.subheader("💡 Analysis Methods Explained")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **📊 Fast Static Analysis**
        - Uses only historical data
        - ⚡ Very fast (< 2 seconds)
        - Based on similar past quotes
        - Good for quick estimates
        - No API calls required
        """)
    
    with col2:
        st.info("""
        **🤖 AI-Powered Analysis**
        - Uses Gemini AI + historical data  
        - ⏱️ Slower (30-60 seconds)
        - Tests multiple discount points
        - More detailed insights
        - Requires API key
        """)'''

    new_help = '''    # Help section
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
    """)'''
    
    if old_help in content:
        content = content.replace(old_help, new_help)
        print("✅ Help section updated")
    
    # Write the file back
    with open('src/app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Static Predictions page updated successfully!")
    return True

if __name__ == "__main__":
    fix_static_predictions()
