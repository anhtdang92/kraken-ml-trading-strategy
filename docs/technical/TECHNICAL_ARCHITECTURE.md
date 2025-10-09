# Technical Architecture Documentation
## Crypto ML Trading Dashboard

**Date:** October 8, 2025  
**Version:** 1.0  
**System Status:** Production Ready ✅

---

## 🏗️ **System Overview**

The Crypto ML Trading Dashboard is a comprehensive Streamlit application that provides cryptocurrency price predictions, portfolio rebalancing, and real-time market data analysis. The system integrates multiple prediction services with intelligent fallback mechanisms.

### **Core Components:**
- **Frontend:** Streamlit web application
- **Prediction Engine:** Hybrid prediction system with multiple providers
- **Data Layer:** Kraken API, BigQuery, Cloud Storage
- **ML Infrastructure:** Vertex AI, TensorFlow, Local models
- **Trading Logic:** Portfolio rebalancing with risk controls

---

## 📊 **Architecture Diagram**

```
┌─────────────────────────────────────────────────────────────────┐
│                    STREAMLIT DASHBOARD                          │
├─────────────────────────────────────────────────────────────────┤
│  Live Prices  │  ML Predictions  │  Portfolio  │  Cloud Progress │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    HYBRID PREDICTION SYSTEM                     │
├─────────────────────────────────────────────────────────────────┤
│  HybridPredictionService  │  PredictionService  │  VertexService │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATA LAYER                                 │
├─────────────────────────────────────────────────────────────────┤
│  Kraken API  │  BigQuery  │  Cloud Storage  │  Local Models    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔧 **Component Details**

### **1. Frontend Layer (Streamlit)**

**File:** `app.py`

**Key Functions:**
- `show_predictions()` - ML prediction display and interaction
- `show_rebalancing()` - Portfolio rebalancing interface
- `show_live_prices()` - Real-time price monitoring
- `show_cloud_progress()` - Cloud infrastructure status

**Features:**
- Multi-page navigation
- Real-time data updates
- Interactive charts (Plotly)
- Responsive design
- Error handling with user feedback

### **2. Prediction Services**

#### **HybridPredictionService** (`ml/hybrid_prediction_service.py`)
**Purpose:** Unified interface combining all prediction methods

**Methods:**
```python
class HybridPredictionService:
    def get_prediction(self, symbol: str, days_ahead: int) -> Dict
    def get_all_predictions(self, symbols: List[str], days_ahead: int) -> Dict[str, Dict]
    def _has_model(self, symbol: str) -> bool
    def train_model(self, symbol: str, days: int, epochs: int) -> Dict
    def train_all_models(self, days: int, epochs: int) -> Dict
    def get_prediction_summary(self) -> Dict
```

**Prediction Priority:**
1. Real ML models (Vertex AI or local)
2. Enhanced mock predictions (technical analysis)
3. Basic mock predictions (fallback)

#### **PredictionService** (`ml/prediction_service.py`)
**Purpose:** Core prediction logic with multiple providers

**Providers:**
- `local` - Enhanced mock predictions
- `vertex` - Vertex AI cloud predictions

#### **VertexPredictionService** (`gcp/deployment/vertex_prediction_service.py`)
**Purpose:** Google Cloud Vertex AI integration

**Features:**
- Model deployment management
- Prediction API calls
- Mock ML predictions fallback
- BigQuery data integration

### **3. Portfolio Management**

#### **PortfolioRebalancer** (`ml/portfolio_rebalancer.py`)
**Purpose:** Portfolio optimization and rebalancing logic

**Key Features:**
- ML-enhanced allocation calculation
- Risk controls and position limits
- Paper trading and live trading modes
- Order generation and execution

**Configuration:**
```python
SUPPORTED_SYMBOLS = ['BTC', 'ETH', 'SOL', 'ADA', 'DOT', 'XRP']
BASE_ALLOCATION = 1.0 / len(SUPPORTED_SYMBOLS)  # Equal weight
MAX_POSITION_WEIGHT = 0.40  # Max 40% per position
MIN_POSITION_WEIGHT = 0.10  # Min 10% per position
ML_WEIGHT_FACTOR = 0.3     # ML influence on allocation
```

### **4. Data Integration**

#### **Kraken API** (`data/kraken_api.py`)
**Purpose:** Real-time cryptocurrency data

**Endpoints Used:**
- `/0/public/Ticker` - Current prices
- `/0/public/OHLC` - Historical data
- `/0/public/AssetPairs` - Trading pairs

#### **BigQuery Integration**
**Purpose:** Historical data storage and analysis

**Tables:**
- `historical_prices` - OHLC data
- `prediction_results` - ML predictions
- `trading_orders` - Order history

#### **Cloud Storage**
**Purpose:** Model artifacts and configuration

**Structure:**
```
gs://crypto-ml-models/
├── models/
│   ├── BTC_model.h5
│   ├── ETH_model.h5
│   └── ...
└── config/
    ├── training_config.json
    └── deployment_config.json
```

---

## 🔄 **Data Flow Architecture**

### **Prediction Flow:**
```
User Request → Mode Selection → Service Router → Prediction Engine → Data Format → Display
     │              │               │              │               │           │
  Symbol +      hybrid/         HybridPrediction  Real ML or      Dict/List   Cards
  Days Ahead    enhanced_mock/  Service          Enhanced Mock    Conversion  Grid
                vertex_ai       Selection        Generation
```

### **Rebalancing Flow:**
```
Portfolio State → ML Predictions → Allocation Calculation → Risk Controls → Orders
       │               │                   │                    │           │
   Current         Enhanced Mock        Weight Adjustment    Position    Buy/Sell
   Holdings        or Real ML           Based on ML          Limits      Orders
```

### **Data Pipeline:**
```
Kraken API → Data Validation → BigQuery → Feature Engineering → ML Training → Model Deployment
     │              │              │              │               │              │
  Real-time       Price/Volume    Historical     Technical      LSTM Model    Vertex AI
  Prices          Validation      Storage        Indicators     Training      Endpoint
```

---

## 🛠️ **Technical Implementation**

### **Error Handling Strategy**

#### **Graceful Degradation:**
```python
try:
    # Primary service
    result = primary_service.operation()
except Exception as e:
    logger.warning(f"Primary failed: {e}, using fallback")
    result = fallback_service.operation()
```

#### **Service Compatibility:**
```python
# Method signature detection
import inspect
sig = inspect.signature(service.get_all_predictions)
if 'symbols' in sig.parameters:
    # HybridPredictionService
    result = service.get_all_predictions(symbols=symbols, days_ahead=days)
else:
    # PredictionService
    result = service.get_all_predictions(days_ahead=days)
```

### **Data Format Standardization**

#### **Prediction Format:**
```python
{
    'symbol': 'BTC',
    'current_price': 45000.0,
    'predicted_price': 46500.0,
    'predicted_return': 0.0333,  # 3.33%
    'confidence': 0.75,
    'days_ahead': 7,
    'prediction_source': 'enhanced_mock',  # or 'vertex_ai_ml', 'local_ml'
    'timestamp': '2025-10-08T22:30:00Z'
}
```

#### **Allocation Format:**
```python
{
    'BTC': 0.1667,  # 16.67% allocation
    'ETH': 0.1667,
    'SOL': 0.1667,
    'ADA': 0.1667,
    'DOT': 0.1667,
    'XRP': 0.1667
}
```

### **Performance Optimizations**

#### **Caching Strategy:**
- Streamlit `@st.cache_data` for expensive operations
- Prediction results cached for 5 minutes
- Model loading cached until restart

#### **Async Operations:**
- Parallel prediction generation for multiple symbols
- Background data fetching
- Non-blocking UI updates

---

## 🔐 **Security & Configuration**

### **Secrets Management:**
```
config/
├── secrets.yaml (gitignored)
├── secrets.yaml.example
└── keys/
    ├── crypto-app-sa-key.json
    ├── ml-prediction-sa-key.json
    └── ml-training-sa-key.json
```

### **Environment Variables:**
```bash
GOOGLE_CLOUD_PROJECT=crypto-ml-trading-487
GCP_REGION=us-central1
VERTEX_ENDPOINT_ID=1074806701011501056
KRAKEN_API_KEY=your_api_key
KRAKEN_SECRET=your_secret
```

### **Access Controls:**
- Service account authentication for GCP
- API key management for Kraken
- Paper trading mode by default
- Confirmation dialogs for live trading

---

## 📈 **Monitoring & Logging**

### **Logging Strategy:**
```python
import logging
logger = logging.getLogger(__name__)

# Prediction operations
logger.info("◊ Generating prediction for BTC")
logger.warning("⚠️ Vertex AI failed for BTC, falling back")
logger.error("❌ Prediction failed for BTC: {error}")

# System status
logger.info("🔀 Hybrid Prediction Service initialized")
logger.info("✅ Generated 6 predictions")
```

### **Health Checks:**
- API connectivity monitoring
- Model availability checks
- Data freshness validation
- System resource monitoring

### **Metrics Tracking:**
- Prediction accuracy
- Response times
- Error rates
- User interactions

---

## 🚀 **Deployment Architecture**

### **Local Development:**
```bash
# Virtual environment
python -m venv venv
source venv/bin/activate

# Dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

### **Cloud Deployment:**
```bash
# GCP setup
gcloud auth login
gcloud config set project crypto-ml-trading-487

# Enable APIs
gcloud services enable aiplatform.googleapis.com
gcloud services enable bigquery.googleapis.com

# Deploy training job
gcloud ai custom-jobs create --config=training_config.yaml

# Deploy endpoint
gcloud ai endpoints deploy-model --endpoint=ENDPOINT_ID
```

### **Docker Configuration:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

---

## 🔧 **Configuration Management**

### **Application Config** (`config/config.yaml`):
```yaml
app:
  title: "Crypto ML Trading Dashboard"
  theme: "dark"
  layout: "wide"

prediction:
  default_mode: "hybrid"
  fallback_enabled: true
  cache_duration: 300  # seconds

trading:
  paper_mode: true
  supported_symbols: ["BTC", "ETH", "SOL", "ADA", "DOT", "XRP"]
  max_position_weight: 0.40
  min_position_weight: 0.10
```

### **Rebalancing Config** (`config/rebalancing_config.json`):
```json
{
  "base_allocation": 0.1667,
  "ml_weight_factor": 0.3,
  "confidence_threshold": 0.6,
  "rebalancing_threshold": 0.05,
  "trading_fee": 0.0016
}
```

---

## 📊 **Performance Metrics**

### **Current Benchmarks:**
- **Prediction Generation:** 2-3 seconds for 6 symbols
- **Page Load Time:** <2 seconds
- **Data Refresh Rate:** 30 seconds
- **Memory Usage:** ~500MB
- **CPU Usage:** Low (mostly I/O bound)

### **Scalability Considerations:**
- **Concurrent Users:** 10-20 users (single instance)
- **Prediction Volume:** 1000+ predictions/hour
- **Data Storage:** 1GB+ historical data
- **Model Size:** 50MB per LSTM model

---

## 🔄 **Backup & Recovery**

### **Data Backup:**
- BigQuery automatic backups
- Cloud Storage versioning
- Local model backups
- Configuration backups

### **Disaster Recovery:**
- Multi-region deployment capability
- Fallback to local models
- Offline mode with cached data
- Configuration restoration procedures

---

## 📝 **Maintenance Procedures**

### **Daily Tasks:**
- Monitor system health
- Check prediction accuracy
- Verify API connectivity
- Review error logs

### **Weekly Tasks:**
- Model performance analysis
- Data quality assessment
- System optimization
- Security updates

### **Monthly Tasks:**
- Model retraining
- Performance tuning
- Capacity planning
- Documentation updates

---

*Technical Architecture Documentation - Last Updated: October 8, 2025*
