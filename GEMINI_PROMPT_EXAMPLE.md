# 🤖 **GEMINI AI PROMPT EXAMPLE WITH YOUR DATA**

## **📊 Using Your test_quotes.csv Data**

Based on your actual test_quotes.csv file, here's **exactly** what gets sent to Gemini AI:

---

## **🎯 EXAMPLE SCENARIO:**
- **Customer**: ABC Logistics (from your data)
- **Route**: India-Mumbai → USA-New York  
- **Shipment**: AIR
- **Commodity**: General
- **Proposed Discount**: 12.5%

---

## **📝 COMPLETE PROMPT SENT TO GEMINI:**

```
You are an AI logistics expert analyzing discount acceptance for quotes.
Based on historical data patterns, predict the likelihood of quote acceptance.

LOGISTICS QUOTE ANALYSIS CONTEXT:

Customer Analysis (ID: ABC LOGISTICS):
- Total historical quotes: 23
- Acceptance rate: 87.0%
- Average accepted discount: 9.8%

Lane Analysis (india_mumbai-usa_new york):
- Total quotes for this lane: 4
- Lane acceptance rate: 100.0%
- Average discount for this lane: 11.2%

Shipment Type Analysis (air):
- Total quotes for this shipment type: 32
- Shipment type acceptance rate: 81.3%
- Average discount for this shipment type: 10.1%

Commodity Analysis (general):
- Total quotes for this commodity: 28
- Commodity acceptance rate: 85.7%
- Average discount for this commodity: 9.5%

CURRENT QUOTE DETAILS:
- Customer ID: ABC LOGISTICS
- Lane: india_mumbai-usa_new york (Original: india_mumbai-usa_new york)
- Shipment Type: air (Original: air)
- Commodity Type: general (Original: general)
- Proposed Discount: 12.5%

Please provide your analysis in the following JSON format:
{
    "acceptance_probability": <float between 0 and 1>,
    "confidence_level": <float between 0 and 1>,
    "key_factors": [<list of key factors influencing the decision>],
    "recommended_discount": <suggested optimal discount percentage>,
    "reasoning": "<detailed explanation of your analysis>",
    "risk_assessment": "<low/medium/high>"
}

Consider factors such as:
- Customer's historical acceptance patterns
- Lane-specific pricing trends
- Shipment type preferences
- Commodity type considerations
- Seasonal factors
- Market conditions
```

---

## **🧠 WHAT GEMINI AI ANALYZES:**

### **📈 Customer Insights (ABC Logistics):**
- **23 total quotes** in your dataset
- **87% acceptance rate** - Very high!
- **Average discount: 9.8%** - Usually accepts lower discounts
- **Pattern**: Consistent customer with strong acceptance

### **🛣️ Lane Performance (India-Mumbai → USA-New York):**
- **4 historical quotes** on this route
- **100% acceptance rate** - Perfect lane performance!
- **Average discount: 11.2%** - Good pricing history
- **Pattern**: Premium route with reliable acceptance

### **📦 Shipment Type (AIR):**
- **32 AIR shipments** in your data
- **81.3% acceptance rate** - Strong performance
- **Average discount: 10.1%** - Standard air freight pricing
- **Pattern**: Air freight generally well-accepted

### **📋 Commodity (General):**
- **28 general cargo quotes**
- **85.7% acceptance rate** - Reliable commodity
- **Average discount: 9.5%** - Conservative pricing
- **Pattern**: Standard cargo, predictable acceptance

---

## **🤖 TYPICAL GEMINI AI RESPONSE:**

```json
{
    "acceptance_probability": 0.92,
    "confidence_level": 0.88,
    "key_factors": [
        "ABC Logistics has exceptional 87% historical acceptance rate",
        "India-Mumbai to USA-New York lane shows perfect 100% acceptance",
        "Proposed 12.5% discount is slightly above average but within acceptable range",
        "AIR shipments for general cargo show consistent acceptance patterns",
        "Customer typically accepts discounts around 9.8%, this is 27% higher but still reasonable"
    ],
    "recommended_discount": 11.0,
    "reasoning": "This quote has very high acceptance probability due to ABC Logistics' excellent track record and the perfect performance of this specific lane. The proposed 12.5% discount is higher than the customer's average (9.8%) but the lane's strong performance (100% acceptance) and the customer's reliability suggest strong acceptance likelihood. Consider offering 11.0% for optimal balance between acceptance and margin.",
    "risk_assessment": "low"
}
```

---

## **💡 KEY INSIGHTS:**

1. **🎯 Rich Context**: Gemini gets deep historical analytics, not just basic data
2. **📊 Multiple Dimensions**: Customer, lane, shipment, commodity patterns all analyzed
3. **🧠 Intelligent Reasoning**: AI considers interactions between different factors
4. **📈 Predictive Power**: Historical patterns help predict future acceptance
5. **💰 Optimization**: AI suggests optimal discount for best acceptance/margin balance

**🚀 This is why your AI predictions are so powerful - Gemini has complete context about your logistics patterns!**
