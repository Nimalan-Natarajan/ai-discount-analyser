# AI-Driven Logistics Quotation Management Tool

A comprehensive application for managing and predicting customer discount acceptance in the logistics industry using AI and statistical analysis.

## Features

### Core Functionality
- **Quote Management**: Process and analyze customer quotations with logistics-specific data
- **AI Prediction**: Predict discount acceptance rates using Google's Gemini API
- **Static Analysis**: Statistical analysis of quote patterns and customer behavior
- **Data Filtering**: Focus analysis on accepted quotes for accurate predictions
- **Lane-Based Analysis**: Analyze discount patterns by origin-destination pairs

### Data Fields Supported
- Customer information with historical discount data
- Quote details: Date, shipment type, commodity type
- Geographic data: Shipper/consignee countries and stations
- Financial data: Discount rates and acceptance status

### Shipment Types
- **AIR**: Air freight shipments
- **OFR FCL**: Ocean Freight Full Container Load
- **OFR LCL**: Ocean Freight Less than Container Load

### Commodity Categories
- General cargo
- Temperature-sensitive goods
- Dangerous goods
- Perishables
- And more...

## Technology Stack

- **Backend**: Python with pandas for data processing
- **AI/ML**: Google Gemini API for predictive analytics
- **Web Interface**: Streamlit for user-friendly dashboard
- **Data Analysis**: NumPy, scikit-learn for statistical analysis
- **Visualization**: Plotly for interactive charts and graphs

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   ```bash
   # Windows
   .\venv\Scripts\Activate.ps1
   
   # Linux/Mac
   source venv/bin/activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Set up your Gemini API key in the `.env` file

## Usage

### Running the Application Locally
```bash
# Windows
.\deploy_prep.bat

# Linux/Mac  
./deploy_prep.sh

# Or manually:
streamlit run src/app.py
```

### 🚀 Deployment
This application is ready for deployment on multiple platforms:

**Recommended: Streamlit Community Cloud (FREE)**
1. Push your code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set main file: `src/app.py`
5. Add your `GEMINI_API_KEY` in secrets
6. Deploy!

See `DEPLOYMENT_STEPS.md` for detailed deployment instructions.

### Data Processing
```python
from src.data_processor import QuoteProcessor

processor = QuoteProcessor()
processed_data = processor.load_and_process('data/quotes.csv')
```

### AI Predictions
```python
from src.ai_predictor import DiscountPredictor

predictor = DiscountPredictor()
prediction = predictor.predict_discount_acceptance(customer_data, quote_details)
```

## Project Structure

```
├── src/
│   ├── app.py                 # Main Streamlit application
│   ├── data_processor.py      # Data processing and cleaning
│   ├── ai_predictor.py        # AI prediction using Gemini API
│   ├── static_analyzer.py     # Statistical analysis functions
│   └── utils/
│       ├── config.py          # Configuration settings
│       └── helpers.py         # Utility functions
├── data/
│   ├── sample_quotes.csv      # Sample data for testing
│   └── processed/             # Processed data files
├── tests/
│   ├── test_data_processor.py
│   ├── test_ai_predictor.py
│   └── test_static_analyzer.py
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## Configuration

Create a `.env` file with your API keys:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
