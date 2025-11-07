# AI-Driven Discount Analyser Tool

A powerful web application for analyzing and predicting customer discount acceptance patterns in the logistics industry. Built with Streamlit and powered by Google's Gemini AI.

## 🌟 Features

### 📊 Dual Analysis Modes
- **Historical Data Analysis**: Lightning-fast statistical analysis of discount patterns (< 2 seconds)
- **AI-Powered Predictions**: Advanced AI analysis using Google Gemini API for detailed insights
- **Interactive Dashboard**: Professional interface with real-time charts and visualizations

### 🚀 Core Capabilities  
- **Smart Data Processing**: Upload and process logistics quotation CSV files
- **Customer Pattern Analysis**: Analyze discount acceptance by customer behavior
- **Lane-Specific Insights**: Optimize pricing for specific origin-destination routes
- **Commodity Intelligence**: Understand discount trends by cargo type
- **Acceptance Rate Optimization**: Find optimal discount ranges for maximum acceptance

### 📁 Supported Data Fields
- Customer IDs and historical discount patterns
- Quote dates and shipment details
- Geographic routes (origin/destination countries and stations)  
- Shipment types: AIR, OFR FCL (Ocean Full Container), OFR LCL (Ocean Less Container)
- Commodity categories: General cargo, temperature-sensitive, dangerous goods, perishables
- Discount rates and acceptance status

## 🛠️ Technology Stack

- **Frontend**: Streamlit web framework for interactive UI
- **Backend**: Python with pandas for efficient data processing
- **AI Engine**: Google Gemini API for intelligent predictions
- **Analytics**: NumPy and scikit-learn for statistical analysis  
- **Visualization**: Plotly for dynamic charts and graphs
- **Deployment**: Streamlit Community Cloud ready

## 🚀 Quick Start

### Option 1: Use the Live App (Recommended)
🌐 **Live Demo**: **[AI Discount Analyser](https://ai-discount-analyser.streamlit.app/)**
- No installation required
- Upload your data and start analyzing immediately
- Enter your own Gemini API key for AI features (optional)

### Option 2: Run Locally
1. **Clone the repository**:
   ```bash
   git clone https://github.com/Nimalan-Natarajan/ai-discount-analyser.git
   cd ai-discount-analyser
   ```

2. **Set up Python environment**:
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate it
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   streamlit run src/app.py
   ```

5. **Open your browser**: Go to `http://localhost:8501`

## 💡 How to Use

### Step 1: Upload Your Data
- Go to **"📁 Data Upload"** page
- Upload a CSV file with your logistics quotation data
- The app will automatically process and validate your data

### Step 2: Analyze with Historical Data (No API Key Required)
- Visit **"📊 Static Predictions"** page  
- Select customer, route, and shipment details
- Click **"📊 Analyze Historical Data"** for instant results
- Get optimal discount recommendations based on past patterns

### Step 3: AI-Powered Analysis (Optional)
- Go to **"⚙️ Settings"** and enter your Gemini API key
- Visit **"🔮 AI Predictions"** page for advanced AI insights
- Get detailed predictions with confidence scores and reasoning

## 🌐 Deployment

### Streamlit Community Cloud (FREE)
1. **Fork this repository** on GitHub
2. **Visit** [share.streamlit.io](https://share.streamlit.io)
3. **Connect your GitHub account** and select the repository
4. **Set main file path**: `src/app.py`
5. **Deploy!** - No API keys or secrets needed
6. **Share your URL** with users

### Key Benefits of This Deployment:
✅ **Zero hosting costs** - Free forever  
✅ **No API costs for you** - Users provide their own Gemini keys  
✅ **Auto-updates** - Syncs with your GitHub repository  
✅ **HTTPS security** - Professional SSL certificates included  
✅ **Global CDN** - Fast loading worldwide

## 🔧 For Developers

### API Usage Examples
```python
# Data Processing
from src.data_processor import QuoteProcessor
processor = QuoteProcessor()
processed_data = processor.load_and_process('data/quotes.csv')

# Static Analysis (No API Key Required)
from src.static_analyzer import StaticAnalyzer
analyzer = StaticAnalyzer()
insights = analyzer.analyze_discount_patterns(processed_data)

# AI Predictions (Requires Gemini API Key)
from src.ai_predictor import DiscountPredictor
predictor = DiscountPredictor()
prediction = predictor.predict_discount_acceptance(
    customer_id="CUST001",
    lane_pair="usa_lax-germany_ham", 
    shipment_type="air",
    commodity_type="general",
    proposed_discount=15.0
)
```

### Project Structure
```
ai-discount-analyser/
├── 🌐 src/
│   ├── app.py                 # Main Streamlit application
│   ├── data_processor.py      # CSV processing and validation  
│   ├── ai_predictor.py        # Gemini AI integration
│   ├── static_analyzer.py     # Fast historical analysis
│   └── utils/
│       ├── config.py          # App configuration
│       └── helpers.py         # Utility functions
├── 📊 data/
│   ├── sample_quotes.csv      # Example data format
│   └── processed/             # Generated analysis files
├── 🧪 tests/
│   ├── test_data_processor.py
│   ├── test_ai_predictor.py  
│   └── test_static_analyzer.py
├── ⚙️ .streamlit/
│   └── config.toml            # Production configuration
├── 📋 requirements.txt        # Python dependencies
├── 🚀 DEPLOYMENT_STEPS.md     # Detailed deployment guide
└── 📖 README.md              # This file
```

## 🔑 API Key Management

**Important**: This app uses **UI-based API key management** - users enter their own keys.

### For Users:
- ✅ Go to Settings page in the app
- ✅ Enter your own Gemini API key  
- ✅ Keys are stored only in your browser session
- ✅ Historical analysis works without any API key

### For Developers:
- ✅ No `.env` files needed
- ✅ No secrets configuration required  
- ✅ No API costs for app hosting
- ✅ Users manage their own quotas and billing

### Get Your Gemini API Key:
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Enter it in the app's Settings page

## 📈 Sample Data Format

Your CSV file should include these columns:
```csv
customer_id,quote_date,shipper_country,shipper_station,consignee_country,consignee_station,shipment_type,commodity_type,discount_offered,status
CUST001,2024-01-15,USA,LAX,Germany,HAM,AIR,general,10.5,accepted
CUST002,2024-01-16,China,SHA,USA,NYC,OFR FCL,electronics,15.0,rejected
```

**Required Fields**:
- `customer_id`: Unique customer identifier
- `shipment_type`: AIR, OFR FCL, or OFR LCL  
- `commodity_type`: Type of goods being shipped
- `discount_offered`: Percentage discount offered
- `status`: accepted or rejected
- Geographic data: Countries and stations

## 🎯 Use Cases

### For Logistics Companies:
- 📊 **Optimize pricing strategies** based on historical acceptance patterns
- 🎯 **Improve win rates** by finding optimal discount ranges
- 📈 **Analyze customer behavior** across different routes and cargo types
- ⚡ **Quick decision support** for sales teams

### For Sales Teams:  
- 💡 Get **instant recommendations** for competitive pricing
- 🔍 **Understand customer preferences** by route and commodity
- 📋 **Track acceptance patterns** to improve future quotes
- 🚀 **Speed up quote generation** with data-driven insights

## 🆘 Troubleshooting

### Common Issues:
**"No data loaded"**: Upload a CSV file in Data Upload section first  
**"Analysis failed"**: Check your CSV format matches the sample  
**"API key invalid"**: Verify your Gemini API key in Settings  
**"Slow performance"**: Use Static Predictions for faster analysis  

### Getting Help:
- 📖 Check `DEPLOYMENT_STEPS.md` for setup issues
- 💬 Open an issue on GitHub for bugs
- 📧 Contact the maintainer for feature requests

## 🤝 Contributing

We welcome contributions! To contribute:

1. **Fork** this repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)  
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🌟 Star This Project

If you find this tool useful, please ⭐ star this repository to help others discover it!

---

**Built with ❤️ for the logistics industry**  
*Helping logistics professionals make data-driven pricing decisions worldwide*
