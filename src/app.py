"""
Main Streamlit application for AI-Driven Discount Analyser Tool
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
import os
from datetime import datetime, timedelta

# Production configuration for deployment
# Note: API keys are handled via UI - users enter their own keys
# No secrets configuration needed for this public deployment model

# Import custom modules
try:
    from .data_processor import QuoteProcessor
    from .ai_predictor import DiscountPredictor
    from .static_analyzer import StaticAnalyzer
    from .utils.config import Config
    from .utils.helpers import setup_logging, validate_discount_range
except ImportError:
    # Fallback for direct execution
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from data_processor import QuoteProcessor
    from ai_predictor import DiscountPredictor
    from static_analyzer import StaticAnalyzer
    from utils.config import Config
    from utils.helpers import setup_logging, validate_discount_range

# Configure page
st.set_page_config(**Config.STREAMLIT_CONFIG)

# Initialize logging
logger = setup_logging()

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None
if 'processor' not in st.session_state:
    st.session_state.processor = QuoteProcessor()
if 'predictor' not in st.session_state:
    st.session_state.predictor = DiscountPredictor()
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = StaticAnalyzer()

def reset_api_key():
    """Utility function to reset API key"""
    # Clear from session state
    st.session_state.gemini_api_key = ""
    
    # Clear from environment completely
    if 'GEMINI_API_KEY' in os.environ:
        del os.environ['GEMINI_API_KEY']
    
    # Also clear any cached API key in the Config module
    try:
        from .utils.config import Config
        Config.GEMINI_API_KEY = None
    except:
        pass
    
    # Reinitialize predictor without API key
    st.session_state.predictor = DiscountPredictor()

def reset_all_data():
    """Utility function to reset all application data (preserves API key)"""
    st.session_state.data_loaded = False
    st.session_state.processed_data = None
    
    # Store current API key before reset
    current_api_key = st.session_state.get('gemini_api_key', '')
    
    # Reinitialize all processors to clear cached data
    st.session_state.processor = QuoteProcessor()
    st.session_state.predictor = DiscountPredictor()
    st.session_state.analyzer = StaticAnalyzer()
    
    # Restore API key if it existed
    if current_api_key:
        st.session_state.gemini_api_key = current_api_key
        os.environ['GEMINI_API_KEY'] = current_api_key
        st.session_state.predictor = DiscountPredictor()  # Reinitialize with API key

def reset_everything():
    """Utility function to reset ALL application data AND API key"""
    # Clear data first (without preserving API key)
    st.session_state.data_loaded = False
    st.session_state.processed_data = None
    
    # Clear API key completely from all sources
    st.session_state.gemini_api_key = ""
    
    # Clear from environment
    if 'GEMINI_API_KEY' in os.environ:
        del os.environ['GEMINI_API_KEY']
    
    # Clear from Config module cache
    try:
        from .utils.config import Config
        Config.GEMINI_API_KEY = None
    except:
        pass
    
    # Reinitialize all processors without any API key
    st.session_state.processor = QuoteProcessor()
    st.session_state.predictor = DiscountPredictor()
    st.session_state.analyzer = StaticAnalyzer()

def main():
    """Main application function"""
    st.title("🚢 AI-Driven Discount Analyser Tool")
    st.markdown("---")
    
    # Sidebar navigation
    page = st.sidebar.selectbox(
        "Navigate to:",
        ["📊 Dashboard", "📁 Data Upload", "🔮 AI Predictions", "📈 Static Analysis", "📊 Static Predictions", "⚙️ Settings"]
    )
    
    # Quick status and management in sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Status")
    
    # Data Status
    if st.session_state.data_loaded:
        st.sidebar.success(f"✅ Data: {len(st.session_state.processed_data)} records")
    else:
        st.sidebar.info("ℹ️ No data loaded")
    
    # API Key Status - Check both session state and environment
    session_api_key = st.session_state.get('gemini_api_key', '')
    env_api_key = os.getenv('GEMINI_API_KEY', '')
    
    if session_api_key or env_api_key:
        st.sidebar.success("🔑 API Key: Configured")
    else:
        st.sidebar.warning("🔑 API Key: Not set")
    
    # Quick Actions
    st.sidebar.subheader("⚡ Quick Actions")
    
    if st.session_state.data_loaded:
        if st.sidebar.button("🔄 Reset Data", help="Clear loaded data only"):
            reset_all_data()
            st.sidebar.success("✅ Data reset!")
            st.rerun()
    
    if session_api_key or env_api_key:
        if st.sidebar.button("🗑️ Reset API Key", help="Clear stored API key"):
            reset_api_key()
            st.sidebar.success("✅ API key reset!")
            st.rerun()
    
    if not st.session_state.data_loaded and not (session_api_key or env_api_key):
        st.sidebar.info("💡 **Get Started:**")
        st.sidebar.markdown("1. Set API key in **Settings**")
        st.sidebar.markdown("2. Upload data in **Data Upload**")
    
    if page == "📁 Data Upload":
        data_upload_page()
    elif page == "📊 Dashboard":
        dashboard_page()
    elif page == "🔮 AI Predictions":
        ai_predictions_page()
    elif page == "📈 Static Analysis":
        static_analysis_page()
    elif page == "📊 Static Predictions":
        quote_optimizer_page()
    elif page == "⚙️ Settings":
        settings_page()

def data_upload_page():
    """Data upload and processing page"""
    st.header("📁 Data Upload & Processing")
    
    # Data Management Section (if data is loaded)
    if st.session_state.data_loaded:
        st.subheader("📊 Current Dataset Management")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Records Loaded", 
                len(st.session_state.processed_data),
                f"Updated: {datetime.now().strftime('%H:%M')}"
            )
        
        with col2:
            st.metric(
                "Customers", 
                st.session_state.processed_data['customer_id'].nunique()
            )
        
        with col3:
            acceptance_rate = (st.session_state.processed_data['status'] == 'accepted').mean()
            st.metric(
                "Acceptance Rate", 
                f"{acceptance_rate:.1%}"
            )
        
        with col4:
            # Reset Data Button with confirmation
            if st.button("🔄 Reset Data", type="secondary"):
                # Show confirmation dialog
                st.warning("⚠️ **Confirm Data Reset**")
                st.write("This will permanently clear all loaded data. Are you sure?")
                
                col_yes, col_no = st.columns(2)
                with col_yes:
                    if st.button("✅ Yes, Reset", type="primary"):
                        reset_all_data()
                        st.success("✅ Data reset successfully! You can now upload a new file.")
                        st.rerun()
                
                with col_no:
                    if st.button("❌ Cancel"):
                        st.rerun()
        
        st.markdown("---")
        st.info("💡 **Ready to upload new data?** Use the Reset Data button above to clear current data and upload a fresh dataset.")
    
    # File Upload Section
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload your quotes CSV file",
        type=['csv'],
        help="Upload a CSV file containing quote data with required columns"
    )
    
    # Show required columns and format specification
    st.subheader("📋 Required CSV Format")
    
    # Show format table
    st.markdown("**Required columns in your CSV file (using test_quotes.csv format):**")
    
    format_data = {
        'Column Name': [
            'date', 'customerName', 'shipmentType', 'commodityType',
            'shipperCountry', 'shipperStation', 'consigneeCountry',
            'consigneeStation', 'discount', 'accepted'
        ],
        'Description': [
            'Quote date (M/D/YYYY format, e.g., 1/15/2024)',
            'Customer name or identifier',
            'AIR, OFR FCL, or OFR LCL', 
            'general, electronics, textiles, etc.',
            'Origin country name or code',
            'Origin station code (e.g., LAX)',
            'Destination country name or code',
            'Destination station code (e.g., HAM)',
            'Discount percentage offered (0-100)',
            'TRUE or FALSE (quote acceptance status)'
        ],
        'Example': [
            '1/15/2024', 'ABC Corp', 'AIR', 'general',
            'USA', 'LAX', 'Germany', 'HAM', '15.5', 'TRUE'
        ]
    }
    
    format_df = pd.DataFrame(format_data)
    st.dataframe(format_df, width='stretch', hide_index=True)
    
    # Show shipment types and commodity types
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Valid Shipment Types:**")
        st.text("• AIR (Air freight)")
        st.text("• OFR FCL (Full Container Load)")
        st.text("• OFR LCL (Less than Container Load)")
    
    with col2:
        st.markdown("**Sample Commodity Types:**")
        st.text("• general, electronics, textiles")
        st.text("• automotive, machinery, perishables")
        st.text("• temperature-sensitive, dangerous goods")
    
    st.info("💡 **Tip**: Download the sample data first to see the exact format expected!")
    
    # Add sample data download
    if os.path.exists("test_quotes.csv"):
        with open("test_quotes.csv", "rb") as file:
            st.download_button(
                label="📥 Download Sample CSV Format (test_quotes.csv)",
                data=file.read(),
                file_name="sample_format_template.csv",
                mime="text/csv",
                help="Download this sample file to see the exact CSV format required"
            )
    elif os.path.exists("data/sample_quotes.csv"):
        # Fallback to original format
        with open("data/sample_quotes.csv", "rb") as file:
            st.download_button(
                label="📥 Download Sample CSV Format",
                data=file.read(),
                file_name="sample_quotes_format.csv",
                mime="text/csv",
                help="Download this sample file to see the exact CSV format required"
            )
    
    if uploaded_file is not None:
        # Clear any existing data to ensure clean override
        if st.session_state.data_loaded:
            st.info("🔄 **Replacing existing data** with new upload...")
            
        try:
            # Validate file size and type
            if uploaded_file.size > 10 * 1024 * 1024:  # 10MB limit
                st.error("❌ File too large. Please keep files under 10MB.")
                return
                
            # Save uploaded file temporarily with safe naming
            import tempfile
            import uuid
            
            # Create safe temporary file
            temp_suffix = f"_{uuid.uuid4().hex[:8]}.csv"
            temp_path = os.path.join(tempfile.gettempdir(), f"upload{temp_suffix}")
            
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.info(f"📁 File uploaded: {uploaded_file.name} ({uploaded_file.size} bytes)")
            
            # Process data with clear feedback
            with st.spinner("🔄 Processing your data..."):
                # Clear existing data first
                st.session_state.processed_data = None
                st.session_state.data_loaded = False
                
                # Process new data with detailed error handling
                try:
                    processed_data = st.session_state.processor.process_data(temp_path)
                except Exception as process_error:
                    st.error(f"❌ Data processing failed: {str(process_error)}")
                    
                    # Show helpful debugging info
                    try:
                        raw_df = pd.read_csv(temp_path)
                        st.info(f"📋 File contains {len(raw_df)} rows and {len(raw_df.columns)} columns")
                        st.info(f"🏷️ Columns found: {list(raw_df.columns)}")
                        
                        # Check if it matches expected format
                        expected_cols = ['date', 'customerName', 'shipmentType', 'commodityType',
                                       'shipperCountry', 'shipperStation', 'consigneeCountry', 
                                       'consigneeStation', 'discount', 'accepted']
                        
                        missing_cols = [col for col in expected_cols if col not in raw_df.columns]
                        if missing_cols:
                            st.error(f"❌ Missing columns: {missing_cols}")
                        else:
                            st.success("✅ All required columns present")
                            
                    except Exception as debug_error:
                        st.error(f"❌ Could not read uploaded file: {debug_error}")
                    
                    return
                
                # Override session state with new data
                st.session_state.processed_data = processed_data
                st.session_state.data_loaded = True
                
                # Load data into predictor and analyzer (fresh)
                st.session_state.predictor.load_historical_data(processed_data)
                st.session_state.analyzer.load_data(processed_data)
            
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            st.success(f"✅ Data processed successfully! Loaded {len(processed_data)} records.")
            
            # Show data summary
            st.subheader("📋 Data Summary")
            summary = st.session_state.processor.get_data_summary()
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Records", summary['total_records'])
            with col2:
                st.metric("Customers", summary['total_customers'])
            with col3:
                st.metric("Lane Pairs", summary['total_lane_pairs'])
            with col4:
                st.metric("Acceptance Rate", f"{summary['acceptance_rate']:.1%}")
            
            # Show data preview
            st.subheader("🔍 Data Preview")
            st.dataframe(processed_data.head(10))
            
        except Exception as e:
            st.error(f"❌ Error processing data: {str(e)}")
            
            # Provide helpful troubleshooting info
            st.info("💡 **Troubleshooting Tips:**")
            st.write("1. **Check file format**: Ensure your CSV matches the test_quotes.csv format")
            st.write("2. **Column names**: Use exact camelCase column names (customerName, shipmentType, etc.)")
            st.write("3. **Data values**: accepted column should have TRUE/FALSE values")
            st.write("4. **Download template**: Use the template download above for reference")
            
            # Log error for debugging
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Data processing error: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())

def dashboard_page():
    """Main dashboard page"""
    st.header("📊 Dashboard Overview")
    
    if not st.session_state.data_loaded:
        st.warning("⚠️ Please upload data first in the 'Data Upload' section.")
        return
    
    df = st.session_state.processed_data
    
    # Key metrics
    st.subheader("🎯 Key Metrics")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Quotes", len(df))
    with col2:
        st.metric("Acceptance Rate", f"{(df['status'] == 'accepted').mean():.1%}")
    with col3:
        st.metric("Avg Discount", f"{df['discount_offered'].mean():.1f}%")
    with col4:
        st.metric("Active Customers", df['customer_id'].nunique())
    with col5:
        st.metric("Active Lanes", df['lane_pair'].nunique())
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Acceptance rate by shipment type
        st.subheader("📦 Acceptance by Shipment Type")
        shipment_stats = df.groupby('shipment_type').agg({
            'status': lambda x: (x == 'accepted').mean()
        }).round(3)
        
        fig = px.bar(
            x=shipment_stats.index,
            y=shipment_stats['status'],
            title="Acceptance Rate by Shipment Type",
            labels={'x': 'Shipment Type', 'y': 'Acceptance Rate'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Discount distribution
        st.subheader("💰 Discount Distribution")
        fig = px.histogram(
            df, x='discount_offered', nbins=20,
            title="Distribution of Discount Offers",
            labels={'discount_offered': 'Discount %', 'count': 'Frequency'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Time series analysis
    st.subheader("📅 Trends Over Time")
    df_monthly = df.set_index('date').resample('M').agg({
        'status': lambda x: (x == 'accepted').mean(),
        'discount_offered': 'mean'
    }).reset_index()
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Scatter(x=df_monthly['date'], y=df_monthly['status'], name="Acceptance Rate"),
        secondary_y=False,
    )
    
    fig.add_trace(
        go.Scatter(x=df_monthly['date'], y=df_monthly['discount_offered'], name="Avg Discount"),
        secondary_y=True,
    )
    
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Acceptance Rate", secondary_y=False)
    fig.update_yaxes(title_text="Average Discount %", secondary_y=True)
    
    st.plotly_chart(fig, use_container_width=True)

def ai_predictions_page():
    """AI prediction page"""
    st.header("🔮 AI-Powered Discount Predictions")
    
    if not st.session_state.data_loaded:
        st.warning("⚠️ Please upload data first in the 'Data Upload' section.")
        return
    
    # Check if Gemini API is configured and working
    current_api_key = st.session_state.get('gemini_api_key', '') or os.getenv('GEMINI_API_KEY', '')
    if not current_api_key:
        st.error("🔑 Gemini API key not configured. Please configure it in the Settings page.")
        st.info("💡 Go to Settings → Enter your Gemini API key to enable AI predictions.")
        return
    
    # Test API connection
    api_status = st.session_state.predictor.model is not None
    if not api_status:
        st.error("❌ Gemini API connection failed. Please check your API key.")
        st.info("🔧 **Troubleshooting:**")
        st.write("1. Verify your API key is valid and active")
        st.write("2. Check if you have API quota remaining")
        st.write("3. Ensure you're using the correct model name")
        
        if st.button("🔄 Test API Connection"):
            try:
                from ai_predictor import DiscountPredictor
                test_predictor = DiscountPredictor()
                available_models = test_predictor.list_available_models()
                
                st.write("**Available Models:**")
                for model in available_models:
                    st.write(f"• {model}")
                    
            except Exception as e:
                st.error(f"API test failed: {str(e)}")
        
        st.info("💡 You can still use static analysis features while fixing the API.")
        return
    
    st.markdown("Use AI to predict customer discount acceptance and get optimization recommendations.")
    
    # Input form
    st.subheader("📝 Quote Details")
    
    df = st.session_state.processed_data
    
    col1, col2 = st.columns(2)
    
    with col1:
        customer_id = st.selectbox(
            "Customer ID",
            options=sorted(df['customer_id'].unique())
        )
        
        shipment_type = st.selectbox(
            "Shipment Type",
            options=Config.SHIPMENT_TYPES
        )
        
        shipper_country = st.selectbox(
            "Shipper Country",
            options=sorted(df['shipper_country'].unique())
        )
        
        consignee_country = st.selectbox(
            "Consignee Country",
            options=sorted(df['consignee_country'].unique())
        )
    
    with col2:
        commodity_type = st.selectbox(
            "Commodity Type",
            options=Config.COMMODITY_TYPES
        )
        
        proposed_discount = st.slider(
            "Proposed Discount (%)",
            min_value=0.0,
            max_value=50.0,
            value=10.0,
            step=0.5
        )
        
        shipper_station = st.text_input("Shipper Station", value="main_port")
        consignee_station = st.text_input("Consignee Station", value="main_port")
    
    # Create lane pair
    lane_pair = f"{shipper_country}_{shipper_station}-{consignee_country}_{consignee_station}"
    
    if st.button("🎯 Get AI Prediction", type="primary"):
        with st.spinner("Getting AI prediction..."):
            prediction = st.session_state.predictor.predict_discount_acceptance(
                customer_id=customer_id,
                lane_pair=lane_pair,
                shipment_type=shipment_type.lower(),
                commodity_type=commodity_type,
                proposed_discount=proposed_discount
            )
        
        # Display results
        st.subheader("🎯 Prediction Results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            prediction_icon = "✅" if prediction['prediction'] == 'likely' else "❌"
            st.metric(
                "Prediction",
                f"{prediction_icon} {prediction['prediction'].title()}",
                f"{prediction['probability']:.1%} probability"
            )
        
        with col2:
            st.metric("Confidence", f"{prediction['confidence']:.1%}")
        
        with col3:
            st.metric("Recommended Discount", f"{prediction['recommended_discount']:.1f}%")
        
        # Risk assessment
        risk_color = {
            'low': '🟢',
            'medium': '🟡',
            'high': '🔴'
        }
        
        st.info(f"**Risk Assessment:** {risk_color.get(prediction['risk_assessment'], '⚪')} {prediction['risk_assessment'].title()}")
        
        # Key factors
        if prediction['key_factors']:
            st.subheader("🔑 Key Factors")
            for factor in prediction['key_factors']:
                st.write(f"• {factor}")
        
        # Detailed reasoning
        if prediction['reasoning']:
            st.subheader("💡 AI Reasoning")
            st.write(prediction['reasoning'])

def static_analysis_page():
    """Static analysis page"""
    st.header("📈 Static Analysis & Insights")
    
    if not st.session_state.data_loaded:
        st.warning("⚠️ Please upload data first in the 'Data Upload' section.")
        return
    
    # Generate comprehensive report
    if st.button("📊 Generate Analysis Report", type="primary"):
        with st.spinner("Generating comprehensive analysis..."):
            report = st.session_state.analyzer.generate_comprehensive_report()
        
        # Overall Statistics
        st.subheader("📊 Overall Statistics")
        overall = report['overall_statistics']
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Quotes", overall['total_quotes'])
        with col2:
            st.metric("Acceptance Rate", f"{overall['overall_acceptance_rate']:.1%}")
        with col3:
            st.metric("Customers", overall['total_customers'])
        with col4:
            st.metric("Lane Pairs", overall['total_lane_pairs'])
        
        # Customer Analysis
        st.subheader("👥 Customer Analysis")
        customer_analysis = report['customer_analysis']
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**High-Value Customers (>70% acceptance):**")
            for customer in customer_analysis['high_value_customers'][:10]:
                st.write(f"• {customer}")
        
        with col2:
            st.write("**Most Active Customers:**")
            for customer in customer_analysis['most_active_customers'][:5]:
                st.write(f"• {customer['customer_id']}: {customer['total_quotes']} quotes ({customer['acceptance_rate']:.1%})")
        
        # Lane Analysis
        st.subheader("🛣️ Lane Performance")
        lane_analysis = report['lane_analysis']
        
        st.write("**Best Performing Lanes:**")
        best_lanes_df = pd.DataFrame(lane_analysis['best_performing_lanes'])
        if not best_lanes_df.empty:
            st.dataframe(best_lanes_df)
        
        # Shipment Type Analysis
        st.subheader("📦 Shipment Type Performance")
        shipment_df = pd.DataFrame(report['shipment_type_analysis']['shipment_type_performance'])
        if not shipment_df.empty:
            fig = px.bar(
                shipment_df,
                x='shipment_type',
                y='acceptance_rate',
                title="Acceptance Rate by Shipment Type"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Discount Sensitivity
        st.subheader("💰 Discount Sensitivity Analysis")
        discount_analysis = report['discount_sensitivity_analysis']
        
        bucket_df = pd.DataFrame(discount_analysis['discount_bucket_analysis'])
        if not bucket_df.empty:
            fig = px.bar(
                bucket_df,
                x='discount_bucket',
                y='acceptance_rate',
                title="Acceptance Rate by Discount Range"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Insights
        st.write("**Key Insights:**")
        for insight in discount_analysis['discount_sensitivity_insights']:
            st.write(f"• {insight}")

def display_optimization_results(optimization, is_static=False):
    """Helper function to display optimization results"""
    method_name = "Static Analysis" if is_static else "AI Analysis"
    st.subheader(f"🎯 {method_name} Results")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Optimal Discount", f"{optimization['optimal_discount']:.1f}%")
    with col2:
        st.metric("Success Probability", f"{optimization['success_probability']:.1%}")
    with col3:
        st.metric("Confidence", f"{optimization['confidence']:.1%}")
    
    if is_static and 'historical_stats' in optimization:
        # Show historical statistics
        st.subheader("📈 Historical Data Analysis")
        stats = optimization['historical_stats']
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Similar Quotes", stats['total_similar_quotes'])
        with col2:
            st.metric("Accepted Quotes", stats['accepted_quotes'])
        with col3:
            st.metric("Avg Discount", f"{stats['average_accepted_discount']:.1f}%")
        with col4:
            st.metric("Median Discount", f"{stats['median_accepted_discount']:.1f}%")
        
        st.info(f"💡 {optimization['recommendation']}")
    
    elif not is_static and 'all_predictions' in optimization:
        # Show AI prediction curve
        predictions_df = pd.DataFrame(optimization['all_predictions'])
        
        fig = px.line(
            predictions_df,
            x='discount',
            y='probability',
            title="Discount vs. Acceptance Probability (AI Analysis)",
            labels={'discount': 'Discount %', 'probability': 'Acceptance Probability'}
        )
        
        # Highlight optimal point
        optimal_point = predictions_df[
            predictions_df['discount'] == optimization['optimal_discount']
        ].iloc[0]
        
        fig.add_scatter(
            x=[optimal_point['discount']],
            y=[optimal_point['probability']],
            mode='markers',
            marker=dict(size=15, color='red'),
            name='Optimal Point'
        )
        
        st.plotly_chart(fig, use_container_width=True)

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
def settings_page():
    """Settings and configuration page"""
    st.header("⚙️ Settings & Configuration")
    
    # API Configuration Section
    st.subheader("🤖 Gemini AI Configuration")
    
    # Initialize session state for API key if not exists
    if 'gemini_api_key' not in st.session_state:
        st.session_state.gemini_api_key = os.getenv('GEMINI_API_KEY', '')
    
    # Ensure API key is propagated to environment if it exists in session
    if st.session_state.gemini_api_key and not os.getenv('GEMINI_API_KEY'):
        os.environ['GEMINI_API_KEY'] = st.session_state.gemini_api_key
    
    # Check current API key status
    current_api_key = st.session_state.gemini_api_key
    
    # Debug information (can be removed later)
    if st.checkbox("🔍 Show Debug Info", help="Show technical details for troubleshooting"):
        st.code(f"""
API Key Sources:
- Session State: {'***' + st.session_state.gemini_api_key[-8:] if st.session_state.gemini_api_key else 'Empty'}
- Environment: {'***' + os.getenv('GEMINI_API_KEY', '')[-8:] if os.getenv('GEMINI_API_KEY') else 'Empty'}
- Config Module: {'***' + Config.GEMINI_API_KEY[-8:] if hasattr(Config, 'GEMINI_API_KEY') and Config.GEMINI_API_KEY else 'Empty'}
- Predictor Model: {st.session_state.predictor.model is not None if st.session_state.predictor else 'No Predictor'}
        """)
    
    # API Key Input
    col1, col2 = st.columns([3, 1])
    
    with col1:
        api_key_input = st.text_input(
            "Gemini API Key",
            value=current_api_key,
            type="password",
            help="Enter your Google Gemini API key. Get one from https://makersuite.google.com/app/apikey",
            placeholder="Enter your Gemini API key here..."
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Add spacing
        col2_1, col2_2 = st.columns(2)
        
        with col2_1:
            if st.button("💾 Save API Key", type="primary"):
                if api_key_input.strip():
                    # Store in session state
                    st.session_state.gemini_api_key = api_key_input.strip()
                    
                    # Update environment variable for current session
                    os.environ['GEMINI_API_KEY'] = api_key_input.strip()
                    
                    # Reinitialize predictor with new API key
                    try:
                        # Use the new reinitialize method
                        if st.session_state.predictor.reinitialize_with_api_key(api_key_input.strip()):
                            # Test the actual API connection
                            is_working, message = st.session_state.predictor.test_api_connection()
                            
                            if is_working:
                                st.success("✅ API key saved and validated successfully!")
                                st.balloons()
                            else:
                                st.warning(f"⚠️ API key saved but validation failed: {message}")
                        else:
                            st.error("❌ Failed to initialize predictor with new API key")
                            
                    except Exception as e:
                        st.error(f"❌ Error initializing with new API key: {str(e)}")
                        
                        # Fallback: try creating a new predictor
                        try:
                            st.session_state.predictor = DiscountPredictor()
                            if st.session_state.predictor.model:
                                st.info("✅ Fallback initialization successful")
                            else:
                                st.error("❌ Fallback initialization also failed")
                        except Exception as fallback_e:
                            st.error(f"❌ Fallback error: {str(fallback_e)}")
                else:
                    st.error("❌ Please enter a valid API key")
        
        with col2_2:
            if st.button("🗑️ Reset API Key", help="Clear stored API key"):
                # Clear API key from session state
                st.session_state.gemini_api_key = ""
                
                # Clear from environment
                if 'GEMINI_API_KEY' in os.environ:
                    del os.environ['GEMINI_API_KEY']
                
                # Reinitialize predictor without API key
                st.session_state.predictor = DiscountPredictor()
                
                st.success("✅ API key reset successfully!")
                st.info("💡 Enter a new API key above to restore AI functionality.")
                st.rerun()
    
    # API Status Display
    st.markdown("---")
    st.subheader("📊 Current API Status")
    
    # Check API status
    api_status_col1, api_status_col2, api_status_col3 = st.columns(3)
    
    with api_status_col1:
        # Check both session state and environment for API key
        session_api_key = st.session_state.get('gemini_api_key', '')
        env_api_key = os.getenv('GEMINI_API_KEY', '')
        
        if session_api_key or env_api_key:
            st.metric("API Key", "✅ Configured", delta="Active")
        else:
            st.metric("API Key", "❌ Missing", delta="Inactive")
    
    with api_status_col2:
        if st.session_state.predictor and st.session_state.predictor.model:
            st.metric("Connection", "✅ Connected", delta="Online")
        else:
            st.metric("Connection", "❌ Failed", delta="Offline")
    
    with api_status_col3:
        if hasattr(st.session_state.predictor, 'current_model_name'):
            model_name = st.session_state.predictor.current_model_name
            st.metric("Active Model", model_name, delta="Working")
        else:
            st.metric("Active Model", "None", delta="Inactive")
    
    # API Key Help Section
    if not current_api_key:
        st.markdown("---")
        st.subheader("🔑 How to Get Your Gemini API Key")
        
        st.info("""
        **Step-by-step guide to get your FREE Gemini API key:**
        
        1. 🌐 **Visit Google AI Studio**: Go to https://makersuite.google.com/app/apikey
        2. 🔐 **Sign in**: Use your Google account to sign in
        3. ➕ **Create API Key**: Click "Create API Key" button
        4. 📋 **Copy Key**: Copy the generated API key (starts with "AIza...")
        5. 📝 **Paste Here**: Paste it in the field above and click "Save API Key"
        
        **💡 Important Notes:**
        - The API key is FREE to use with generous quotas
        - Keep your API key secure and don't share it publicly  
        - You can regenerate the key anytime if needed
        - No credit card required for basic usage
        """)
        
        st.markdown("""
        **🔗 Quick Links:**
        - 🔑 [Get Free API Key](https://makersuite.google.com/app/apikey)
        - 📚 [Gemini API Documentation](https://ai.google.dev/docs)
        - 💰 [Pricing Information](https://ai.google.dev/pricing)
        """)
    
    # Test API Connection
    if current_api_key:
        st.markdown("---")
        st.subheader("🧪 Test API Connection")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("🔍 Test Connection", help="Send a test request to verify your API key works"):
                with st.spinner("Testing API connection..."):
                    try:
                        # Use the predictor's built-in test method
                        if st.session_state.predictor and hasattr(st.session_state.predictor, 'test_api_connection'):
                            is_working, message = st.session_state.predictor.test_api_connection()
                            
                            if is_working:
                                st.success("✅ API connection test successful!")
                                st.json({
                                    "status": "success",
                                    "model": st.session_state.predictor.current_model_name or "Unknown",
                                    "message": message,
                                    "details": "Your API key is working correctly!"
                                })
                            else:
                                st.error(f"❌ API connection test failed: {message}")
                                
                                # Provide helpful troubleshooting
                                if "403" in message:
                                    st.info("💡 **403 Forbidden**: Check if your API key is valid and has proper permissions")
                                elif "404" in message:
                                    st.info("💡 **404 Not Found**: The model might not be available. Try a different model.")
                                elif "quota" in message.lower():
                                    st.info("💡 **Quota Exceeded**: You've hit your API usage limit. Wait or upgrade your plan.")
                                else:
                                    st.info("💡 Check your API key, internet connection, or try again later")
                        else:
                            # Fallback to direct test if predictor method not available
                            import google.generativeai as genai
                            genai.configure(api_key=current_api_key)
                            
                            test_model = genai.GenerativeModel('gemini-2.5-flash')
                            response = test_model.generate_content("Say 'API Test OK'")
                            
                            st.success("✅ API connection test successful!")
                            st.json({
                                "status": "success",
                                "model": "gemini-2.5-flash",
                                "response": response.text.strip(),
                                "message": "Your API key is working correctly!"
                            })
                        
                    except Exception as e:
                        st.error(f"❌ API connection test failed: {str(e)}")
                        
                        if "403" in str(e):
                            st.info("💡 **403 Forbidden**: Check if your API key is valid and has proper permissions")
                        elif "404" in str(e):
                            st.info("💡 **404 Not Found**: The model might not be available. This is normal - the system will use fallback models.")
                        else:
                            st.info("💡 Try checking your API key or internet connection")
        
        with col2:
            if st.button("🔍 Discover Models", help="See what Gemini models are available"):
                with st.spinner("Discovering available models..."):
                    try:
                        available_models = st.session_state.predictor.discover_working_models()
                        
                        if available_models:
                            st.success(f"✅ Found {len(available_models)} available models:")
                            for i, model in enumerate(available_models, 1):
                                st.write(f"{i}. **{model}**")
                        else:
                            st.warning("⚠️ No models discovered. Check your API key.")
                            
                    except Exception as e:
                        st.error(f"❌ Error discovering models: {str(e)}")
    
    # Model Selection (Advanced)
    if current_api_key and st.session_state.predictor:
        st.markdown("---")
        st.subheader("🎛️ Advanced Settings")
        
        with st.expander("🤖 Model Selection", expanded=False):
            st.info("The system automatically selects the best available Gemini model. Advanced users can view available models here.")
            
            if st.button("🔍 Discover Available Models"):
                with st.spinner("Discovering models..."):
                    try:
                        available_models = st.session_state.predictor.discover_working_models()
                        
                        if available_models:
                            st.success(f"Found {len(available_models)} available models:")
                            for i, model in enumerate(available_models, 1):
                                st.write(f"{i}. **{model}**")
                        else:
                            st.warning("No models discovered. Check your API key.")
                            
                    except Exception as e:
                        st.error(f"Error discovering models: {str(e)}")
    
    # Data Storage Settings
    st.markdown("---") 
    st.subheader("💾 Data Storage")
    
    st.info("""
    **📋 Current Storage Status:**
    - ✅ All data is stored locally in your browser session
    - ✅ No data is sent to external servers (except Gemini API for predictions)
    - ✅ Your API key is stored securely in the session
    - 🔄 Data clears when you refresh/close the browser
    """)
    
    # Data Management Actions
    col1, col2, col3 = st.columns(3)
    
    if st.session_state.data_loaded:
        with col1:
            if st.button("🗑️ Clear Data Only", help="Remove uploaded data but keep API key", type="secondary"):
                st.warning("⚠️ **Confirm Data Reset**")
                st.write("This will clear loaded data but preserve your API key.")
                
                if st.button("⚠️ Confirm Clear Data", help="This will permanently remove all loaded data", type="primary"):
                    reset_all_data()
                    st.success("✅ Data cleared successfully! API key preserved.")
                    st.rerun()
        
        with col2:
            if st.session_state.processed_data is not None:
                # Create download for current data
                csv_data = st.session_state.processed_data.to_csv(index=False)
                st.download_button(
                    "📥 Download Current Data",
                    data=csv_data,
                    file_name=f"processed_quotes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    help="Download your currently processed data"
                )
        
        with col3:
            # Data statistics
            st.metric(
                "Current Dataset", 
                f"{len(st.session_state.processed_data)} records",
                f"{st.session_state.processed_data['customer_id'].nunique()} customers"
            )
    else:
        with col1:
            st.info("ℹ️ No data currently loaded")
        
        with col2:
            st.info("ℹ️ Upload data first to enable downloads")
        
        with col3:
            st.info("ℹ️ Dataset statistics will appear here")
    
    # Complete Reset Section
    st.markdown("---")
    st.subheader("🔥 Complete Application Reset")
    
    st.warning("⚠️ **Danger Zone**: These actions will reset ALL application data and settings.")
    
    # Use session state to handle confirmations (avoid nested buttons)
    if 'confirm_api_reset' not in st.session_state:
        st.session_state.confirm_api_reset = False
    if 'confirm_complete_reset' not in st.session_state:
        st.session_state.confirm_complete_reset = False
    
    col1, col2 = st.columns(2)
    
    with col1:
        if not st.session_state.confirm_api_reset:
            if st.button("🗑️ Reset API Key Only", help="Clear only the stored API key", type="secondary"):
                st.session_state.confirm_api_reset = True
                st.rerun()
        else:
            st.error("⚠️ **Confirm API Key Reset**")
            st.write("This will permanently clear your stored API key. You'll need to re-enter it.")
            
            col_yes, col_no = st.columns(2)
            with col_yes:
                if st.button("✅ Yes, Reset API Key", type="primary"):
                    reset_api_key()
                    st.session_state.confirm_api_reset = False
                    st.success("✅ API key reset successfully!")
                    st.rerun()
            
            with col_no:
                if st.button("❌ Cancel", type="secondary"):
                    st.session_state.confirm_api_reset = False
                    st.rerun()
    
    with col2:
        if not st.session_state.confirm_complete_reset:
            if st.button("💥 Reset Everything", help="Clear ALL data and API key", type="secondary"):
                st.session_state.confirm_complete_reset = True
                st.rerun()
        else:
            st.error("⚠️ **CONFIRM COMPLETE RESET**")
            st.write("This will permanently clear ALL data, settings, and API key. You'll start completely fresh.")
            
            col_confirm, col_nuclear, col_cancel = st.columns(3)
            
            with col_confirm:
                if st.button("💥 Complete Reset", type="primary"):
                    reset_everything()
                    st.session_state.confirm_complete_reset = False
                    st.success("✅ Complete application reset successful!")
                    st.info("🔄 **Please refresh your browser** (F5 or Ctrl+R) to ensure all cached data is cleared.")
                    st.rerun()
            
            with col_nuclear:
                if st.button("🧨 Nuclear Reset", type="primary"):
                    # Clear ALL session state
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    
                    # Clear all environment variables we might have set
                    env_keys_to_clear = ['GEMINI_API_KEY']
                    for key in env_keys_to_clear:
                        if key in os.environ:
                            del os.environ[key]
                    
                    st.success("🧨 NUCLEAR RESET COMPLETE!")
                    st.error("🔄 **REFRESH YOUR BROWSER NOW** (F5 or Ctrl+R)")
                    
                    # Add JavaScript to force browser refresh after a short delay
                    st.markdown("""
                    <script>
                    setTimeout(function(){
                        window.location.reload();
                    }, 2000);
                    </script>
                    """, unsafe_allow_html=True)
                    
                    st.stop()  # Stop execution to force user to refresh
            
            with col_cancel:
                if st.button("❌ Cancel Reset", type="secondary"):
                    st.session_state.confirm_complete_reset = False
                    st.rerun()

if __name__ == "__main__":
    main()
