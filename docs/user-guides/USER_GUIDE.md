# User Guide
## Crypto ML Trading Dashboard

**Welcome to your advanced cryptocurrency trading dashboard!** 🚀

This guide will help you navigate and use all the features of your ML-powered trading system.

---

## 🎯 **Getting Started**

### **Accessing the Dashboard**
1. **Start the application:**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser:**
   - Navigate to `http://localhost:8501`
   - The dashboard will load automatically

3. **First-time setup:**
   - All systems are pre-configured
   - Paper trading is enabled by default (safe mode)
   - No additional setup required

---

## 📊 **Dashboard Overview**

### **Navigation Menu (Sidebar)**
- **🏠 Portfolio Overview** - Current holdings and performance
- **📈 Live Prices** - Real-time cryptocurrency prices
- **🧠 ML Predictions** - AI-powered price predictions
- **⚖️ Portfolio Rebalancing** - Automated portfolio optimization
- **☁️ Cloud Progress** - Training and deployment status
- **🔧 Nova Console** - Advanced system controls

### **Main Content Area**
- **Dynamic pages** that change based on your selection
- **Real-time data updates** every 30 seconds
- **Interactive charts** and visualizations
- **Responsive design** that works on all devices

---

## 🧠 **ML Predictions Page**

### **Prediction Modes**

#### **🔀 Hybrid Mode (Recommended)**
**Best of both worlds - combines real ML with reliable fallbacks**

**Features:**
- ✅ **Real ML Models** when available (Vertex AI or local)
- ✅ **Enhanced Mock Predictions** with technical analysis as fallback
- ✅ **Automatic failover** ensures predictions always work
- ✅ **Source transparency** - see which method was used

**When to use:** Always - this is the most reliable option

#### **🏠 Enhanced Mock Mode**
**Reliable predictions using technical analysis**

**Features:**
- ✅ **Real-time Kraken API data**
- ✅ **Technical analysis** (RSI, trends, volatility)
- ✅ **Dynamic confidence scoring**
- ✅ **Always available** - no training required

**When to use:** When you want consistent, reliable predictions

#### **☁️ Vertex AI Mode**
**Real trained machine learning models**

**Features:**
- ✅ **Actual ML models** trained on historical data
- ✅ **Advanced LSTM neural networks**
- ✅ **Cloud-powered predictions**
- ⚠️ **Fallback to mock** if models aren't deployed

**When to use:** When real ML models are deployed and working

### **Using Predictions**

1. **Select a cryptocurrency:**
   - Choose "All" for comprehensive overview
   - Or select specific symbols (BTC, ETH, SOL, ADA, DOT, XRP)

2. **Choose prediction timeframe:**
   - 7 days (default)
   - 14 days
   - 30 days

3. **View results:**
   - **Prediction cards** show expected returns
   - **Color coding:** Green (bullish), Red (bearish)
   - **Confidence scores** indicate prediction reliability
   - **Source badges** show which method was used

### **Understanding Prediction Results**

#### **Return Predictions:**
- **Positive values** (green): Expected price increase
- **Negative values** (red): Expected price decrease
- **Percentage format:** Easy to understand (e.g., +3.5% = 3.5% gain expected)

#### **Confidence Scores:**
- **0.8-1.0:** Very high confidence (reliable predictions)
- **0.6-0.8:** High confidence (good predictions)
- **0.4-0.6:** Medium confidence (moderate reliability)
- **Below 0.4:** Low confidence (use with caution)

#### **Source Indicators:**
- **🔀 Hybrid:** Combined approach used
- **☁️ Vertex AI:** Real ML model prediction
- **🏠 Enhanced Mock:** Technical analysis prediction
- **📊 Local ML:** Local trained model used

---

## ⚖️ **Portfolio Rebalancing Page**

### **Rebalancing Modes**

#### **🔀 Hybrid Rebalancing (Recommended)**
**Uses hybrid predictions for optimal allocation**

**Benefits:**
- ✅ **Best prediction accuracy** from combined sources
- ✅ **Robust fallbacks** ensure rebalancing always works
- ✅ **ML-enhanced allocations** for better returns
- ✅ **Risk-controlled adjustments**

#### **🏠 Enhanced Mock Rebalancing**
**Uses technical analysis for allocation decisions**

**Benefits:**
- ✅ **Consistent performance** with reliable predictions
- ✅ **Always available** regardless of ML model status
- ✅ **Technical indicator-based** adjustments
- ✅ **Stable rebalancing** logic

#### **☁️ Vertex AI Rebalancing**
**Uses real ML models for allocation optimization**

**Benefits:**
- ✅ **Advanced ML insights** for allocation decisions
- ✅ **Data-driven optimization** based on trained models
- ✅ **Cloud-powered processing** for complex calculations
- ⚠️ **Fallback available** if models aren't ready

### **Rebalancing Process**

1. **Current Portfolio Analysis:**
   - View your current holdings
   - See current allocation percentages
   - Identify drift from target allocation

2. **Target Allocation Calculation:**
   - **Base allocation:** Equal weight (16.67% each for 6 symbols)
   - **ML adjustments:** Enhanced based on predictions
   - **Risk controls:** Position limits applied
   - **Final allocation:** Optimized target weights

3. **Order Generation:**
   - **Buy orders:** For underweight positions
   - **Sell orders:** For overweight positions
   - **Order sizing:** Calculated precisely
   - **Fee consideration:** Trading costs included

4. **Execution Options:**
   - **Paper Trading:** Simulate trades (default, safe)
   - **Live Trading:** Execute real trades (requires confirmation)

### **Understanding Rebalancing Results**

#### **Allocation Comparison:**
- **Current vs Target:** See how your portfolio needs to change
- **Drift Analysis:** Identify which positions are off-target
- **Rebalancing Threshold:** Only rebalance when drift > 5%

#### **Order Details:**
- **Symbol:** Which cryptocurrency to trade
- **Action:** Buy or Sell
- **Quantity:** How much to trade
- **Estimated Cost:** Including fees
- **Reason:** Why this trade is recommended

#### **Risk Metrics:**
- **Total Portfolio Value:** Current worth
- **Expected Return:** Based on ML predictions
- **Risk Score:** Portfolio volatility assessment
- **Sharpe Ratio:** Risk-adjusted return measure

---

## 📈 **Live Prices Page**

### **Real-Time Data**
- **Current prices** from Kraken exchange
- **24h change** in price and percentage
- **Volume data** for trading activity
- **Price charts** with interactive features

### **Interactive Charts**
- **Zoom and pan** on price history
- **Time range selection** (1D, 7D, 30D)
- **Volume overlay** for market analysis
- **Mobile-friendly** responsive design

---

## 🏠 **Portfolio Overview Page**

### **Portfolio Summary**
- **Total value** of your holdings
- **Day change** in portfolio value
- **Allocation breakdown** by cryptocurrency
- **Performance metrics** and charts

### **Allocation Visualization**
- **Pie charts** showing current allocation
- **Target vs actual** comparison
- **Rebalancing recommendations** if needed
- **Historical performance** tracking

---

## ☁️ **Cloud Progress Page**

### **Training Status**
- **Current training jobs** and their progress
- **Model deployment** status
- **Training metrics** and results
- **Cost tracking** for cloud resources

### **Endpoint Status**
- **Vertex AI endpoints** availability
- **Model deployment** progress
- **Prediction service** health
- **Performance metrics**

---

## 🔧 **Nova Console (Advanced)**

### **System Controls**
- **Prediction service** configuration
- **Model training** controls
- **Data refresh** operations
- **System diagnostics**

### **Developer Tools**
- **Log viewing** and analysis
- **Configuration** management
- **API testing** tools
- **Performance monitoring**

---

## ⚙️ **Configuration Options**

### **Trading Settings**
- **Paper Trading Mode:** Safe simulation (default: ON)
- **Live Trading Mode:** Real trades (requires confirmation)
- **Position Limits:** Maximum allocation per symbol
- **Rebalancing Threshold:** When to trigger rebalancing

### **Prediction Settings**
- **Default Mode:** Hybrid (recommended)
- **Prediction Horizon:** 7 days (default)
- **Confidence Threshold:** Minimum confidence for ML adjustments
- **Fallback Behavior:** Automatic or manual

### **Risk Management**
- **Maximum Position Weight:** 40% per symbol (default)
- **Minimum Position Weight:** 10% per symbol (default)
- **ML Weight Factor:** 30% ML influence on allocation
- **Trading Fees:** 0.16% maker fee (Kraken)

---

## 🚨 **Safety Features**

### **Paper Trading (Default)**
- ✅ **All trades are simulated** - no real money at risk
- ✅ **Full functionality** without financial risk
- ✅ **Learning environment** to understand the system
- ✅ **Performance tracking** without consequences

### **Live Trading Safeguards**
- ⚠️ **Confirmation dialogs** for all real trades
- ⚠️ **Position limits** prevent over-concentration
- ⚠️ **Risk controls** built into all decisions
- ⚠️ **Audit trail** for all trading activity

### **Error Handling**
- ✅ **Graceful fallbacks** when services fail
- ✅ **User-friendly error messages**
- ✅ **Automatic recovery** from temporary issues
- ✅ **Comprehensive logging** for troubleshooting

---

## 💡 **Tips for Best Results**

### **Getting Started:**
1. **Start with Paper Trading** to learn the system
2. **Use Hybrid Mode** for the most reliable predictions
3. **Monitor predictions** for a few days before live trading
4. **Understand the risk controls** and position limits

### **Optimizing Performance:**
1. **Regular rebalancing** based on ML recommendations
2. **Monitor prediction accuracy** over time
3. **Adjust confidence thresholds** based on your risk tolerance
4. **Review portfolio performance** weekly

### **Risk Management:**
1. **Never invest more than you can afford to lose**
2. **Diversify beyond cryptocurrencies** in your overall portfolio
3. **Monitor market conditions** and adjust accordingly
4. **Use position limits** to prevent over-concentration

---

## 🆘 **Troubleshooting**

### **Common Issues:**

#### **"No predictions available"**
- **Cause:** API connectivity issues
- **Solution:** Check internet connection, refresh page
- **Fallback:** System will retry automatically

#### **"Prediction service failed"**
- **Cause:** Temporary service unavailability
- **Solution:** System automatically falls back to enhanced mock
- **Note:** Predictions will still work with fallback

#### **"Model not trained"**
- **Cause:** ML models haven't been trained yet
- **Solution:** Use enhanced mock mode, or wait for training completion
- **Note:** Enhanced mock predictions are still highly effective

#### **"Rebalancing not recommended"**
- **Cause:** Portfolio is within rebalancing threshold
- **Solution:** Wait for more significant drift, or manually adjust
- **Note:** This prevents unnecessary trading fees

### **Getting Help:**
- **Check the logs** in Nova Console for detailed error information
- **Review system status** in Cloud Progress page
- **Monitor prediction accuracy** to understand system performance
- **Use paper trading** to test changes safely

---

## 📚 **Additional Resources**

### **Understanding the Technology:**
- **LSTM Neural Networks:** How the ML models work
- **Technical Analysis:** RSI, moving averages, volatility indicators
- **Portfolio Theory:** Modern portfolio optimization principles
- **Risk Management:** Position sizing and diversification

### **Best Practices:**
- **Start small** and scale up as you gain confidence
- **Monitor performance** regularly and adjust strategies
- **Stay informed** about market conditions and news
- **Diversify** your overall investment portfolio

---

**🎉 Congratulations! You now have access to one of the most advanced cryptocurrency trading dashboards available. Start with paper trading, learn the system, and gradually scale up your usage as you become comfortable with the technology.**

---

*User Guide - Last Updated: October 8, 2025*
