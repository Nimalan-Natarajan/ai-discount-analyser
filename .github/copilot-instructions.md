# Copilot Instructions for Logistics Quotation Management Tool

<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

## Project Overview
This is an AI-driven quotation management tool for the logistics industry that predicts customer discount acceptance rates.

## Key Components
- **Data Processing**: Handle customer quotes with logistics-specific fields (shipment types, commodities, lanes)
- **AI Prediction**: Use Gemini API for discount prediction based on historical data
- **Static Analysis**: Provide statistical analysis of quote acceptance patterns
- **Web Interface**: Streamlit-based UI for quote management and predictions

## Domain-Specific Context
- **Shipment Types**: AIR, OFR FCL (Ocean Freight Full Container Load), OFR LCL (Ocean Freight Less than Container Load)
- **Commodity Types**: General cargo, temperature-sensitive, dangerous goods, perishables
- **Lane Pairs**: Origin-destination combinations (country/station pairs)
- **Discount Analysis**: Focus on accepted quotes for training AI models

## Code Style Guidelines
- Use pandas for data manipulation
- Implement proper error handling for API calls
- Follow logistics industry naming conventions
- Structure code for scalability and maintainability
- Include comprehensive logging for debugging

## AI/ML Considerations
- Train models on accepted quotes only
- Consider seasonal patterns in logistics
- Handle imbalanced datasets (more rejected than accepted quotes)
- Implement feature engineering for lane-specific patterns
