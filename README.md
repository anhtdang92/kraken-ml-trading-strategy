# ⚡ NOVA - Crypto Intelligence System

> **AI-Powered Cryptocurrency Trading Dashboard with Machine Learning Price Predictions**

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Google_Cloud-blue)
![Python](https://img.shields.io/badge/python-3.9+-blue)

A futuristic cyberpunk-themed cryptocurrency trading dashboard powered by LSTM neural networks, real-time Kraken API integration, and Google Cloud ML infrastructure.

---

## ✨ Features

### 🎨 Cyberpunk UI
- **Dark mode only** with neon aesthetics
- **Liquid glass** morphism effects
- **Font Awesome** icons with neon glows
- **Orbitron & Rajdhani** futuristic fonts
- **Animated** scan lines and effects

### 📊 Portfolio Management
- **Real-time** Kraken portfolio sync
- **Live price** updates
- **Staking tracking** (bonded/locked assets)
- **P&L calculations** with visual indicators
- **Asset allocation** pie charts

### 🧠 ML Price Predictions
- **LSTM neural networks** (2-layer, 50 units)
- **11 technical indicators** (MA, RSI, volume, etc.)
- **Hybrid system**: Real ML + Enhanced Mock
- **Confidence scoring** for each prediction
- **7-day forecasts** for 6 major cryptos

### ⚖️ Portfolio Rebalancing
- **ML-enhanced allocation** strategy
- **Risk controls** (position limits, trade minimums)
- **Paper trading** mode for testing
- **Fee optimization** (0.16% Kraken maker fees)
- **Real-time** rebalancing recommendations

### ☁️ Cloud ML Training
- **Google Cloud** Vertex AI integration
- **Budget-optimized** ($3-8 per training run)
- **Real-time** progress tracking
- **Auto-scaling** prediction endpoints
- **Live training** logs in dashboard

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 2. Configure Kraken API
```bash
# Copy example config
cp config/secrets.yaml.example config/secrets.yaml

# Edit config/secrets.yaml with your Kraken API keys
# Get API keys from: https://www.kraken.com/u/security/api
```

### 3. Run the Dashboard
```bash
streamlit run app.py
```

Open: **http://localhost:8501**

---

## 🧠 Train ML Models (Google Cloud)

### First-Time Setup (5 minutes)
```bash
# Run setup wizard
./bin/quick-start.sh
```

### Train Models
```bash
# Interactive training launcher
./bin/train_now.sh

# Choose option 1: Budget Training ($3-8, 30-60 min)
```

### Track Progress
- **Dashboard:** http://localhost:8501 → ☁️ Cloud Progress
- **Terminal:** `./bin/check_training.sh`
- **Web:** [Vertex AI Console](https://console.cloud.google.com/vertex-ai)

---

## 📁 Project Structure

```
Kraken_Cloud_ML_Strat/
│
├── 📱 app.py                 # Main Streamlit dashboard
├── 📋 requirements.txt       # Dependencies
│
├── 🚀 bin/                   # User scripts
│   ├── train_now.sh         # Train ML models
│   ├── check_training.sh    # Check training status
│   ├── quick-start.sh       # First-time setup
│   └── dev-setup.sh         # Development setup
│
├── ⚙️  config/               # Configuration
│   ├── config.yaml          # App settings
│   ├── gcp_config.yaml      # Google Cloud config
│   └── keys/                # Service account keys (gitignored)
│
├── 📊 data/                  # Kraken API clients
│   ├── kraken_api.py        # Public API
│   └── kraken_auth.py       # Private API (auth required)
│
├── 🧠 ml/                    # Machine Learning
│   ├── prediction_service.py           # Main ML service
│   ├── hybrid_prediction_service.py    # Hybrid predictions
│   ├── lstm_model.py                   # LSTM architecture
│   ├── feature_engineering.py          # Technical indicators
│   ├── historical_data_fetcher.py      # Data collection
│   └── portfolio_rebalancer.py         # Rebalancing logic
│
├── ☁️  gcp/                  # Google Cloud Platform
│   ├── training/            # ML training containers
│   ├── deployment/          # Prediction services
│   ├── cloud_functions/     # Serverless functions
│   └── scripts/             # GCP automation
│       ├── setup/           # One-time infrastructure setup
│       ├── training/        # Training job deployment
│       └── deployment/      # Endpoint deployment
│
├── 📦 models/                # Trained models (gitignored)
├── 🧪 tests/                 # Unit & integration tests
├── 📚 docs/                  # Documentation
└── 📁 archive/               # Old/backup files
```

---

## 📚 Documentation

- **[Quick Start Guide](docs/user-guides/QUICKSTART.md)** - Get started in 5 minutes
- **[ML Training Guide](docs/user-guides/TRAIN_ML_MODELS.md)** - Train models on GCP
- **[UI Guide](docs/user-guides/UI_IMPROVEMENTS.md)** - UI features & design
- **[GCP Setup](docs/deployment/GCP_ML_SETUP_GUIDE.md)** - Cloud infrastructure
- **[Technical Architecture](docs/technical/TECHNICAL_ARCHITECTURE.md)** - System design

---

## 💰 Costs (Google Cloud)

| Service | Monthly Cost | Optimization |
|---------|--------------|--------------|
| Vertex AI Training | $5-10 | Preemptible instances (60% off) |
| Prediction Endpoint | $10-15 | Auto-scaling, scale-to-zero |
| BigQuery | $2-5 | Partitioned tables |
| Cloud Storage | $1-2 | Lifecycle policies |
| **Total** | **$18-32** | **~3 months on $50 credit** |

---

## 🎯 Supported Cryptocurrencies

1. **BTC** (Bitcoin)
2. **ETH** (Ethereum)
3. **SOL** (Solana)
4. **ADA** (Cardano)
5. **DOT** (Polkadot)
6. **XRP** (Ripple)

---

## 🛠️ Technology Stack

**Frontend:**
- Streamlit (Dashboard)
- Plotly (Charts)
- Font Awesome (Icons)

**ML/AI:**
- TensorFlow 2.13 (LSTM models)
- Google Vertex AI (Cloud training)
- Scikit-learn (Preprocessing)
- NumPy, Pandas (Data processing)

**Data:**
- Kraken API (Real-time prices)
- Google BigQuery (Data storage)
- Cloud Storage (Model artifacts)

**Infrastructure:**
- Google Cloud Platform
- Docker (Containerization)
- GitHub Actions (CI/CD)

---

## 📊 Dashboard Pages

### ⚡ Portfolio
- Real-time Kraken portfolio sync
- Liquid & staked asset tracking
- P&L calculations
- Allocation charts

### ↗ Live Prices
- Real-time crypto prices
- Interactive candlestick/line charts
- 24h statistics (high, low, volume)
- 6 major cryptocurrencies

### ◉ ML Predictions
- LSTM neural network predictions
- 7-day price forecasts
- Confidence scores
- Hybrid prediction system
- Model training interface

### ◉ Rebalancing
- ML-enhanced allocation
- Target vs current comparison
- Order generation with fees
- Paper trading mode
- Portfolio health metrics

### ☁️ Cloud Progress
- Real-time training status
- Live job logs
- Cost tracking
- Progress timeline
- System health monitoring

---

## 🔐 Security

- ✅ API keys stored in `config/keys/` (gitignored)
- ✅ Service accounts with minimal permissions
- ✅ Paper trading mode by default
- ✅ No private keys in code
- ✅ Encrypted communication with Kraken

---

## 🧪 Testing

```bash
# Run unit tests
python -m pytest tests/unit/

# Run integration tests
python -m pytest tests/integration/

# Test Kraken connection
python tests/unit/kraken_test.py

# Test GCP connection
python tests/unit/test_gcp.py
```

---

## 📈 Performance

- **Prediction speed:** <100ms per crypto
- **Data refresh:** 60-second cache
- **Dashboard load:** <2 seconds
- **Training time:** 30-60 minutes (4 cryptos)
- **Inference:** <50ms via Vertex AI endpoint

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ⚠️ Disclaimer

This software is for **educational and research purposes only**. Cryptocurrency trading involves substantial risk of loss. Past performance does not guarantee future results. Always do your own research before making investment decisions.

---

## 🆘 Support

- **Issues:** [GitHub Issues](https://github.com/anhtdang92/Kraken_Cloud_ML_Strat/issues)
- **Documentation:** See `docs/` folder
- **Email:** Your email here

---

## 🎯 Roadmap

- [x] Real-time portfolio tracking
- [x] LSTM price predictions
- [x] Google Cloud ML training
- [x] Portfolio rebalancing
- [x] Cyberpunk UI theme
- [ ] Automated trading execution
- [ ] Multi-exchange support
- [ ] Mobile app
- [ ] Trading bot automation
- [ ] Advanced risk management

---

## 🌟 Star This Repo!

If you find this project useful, please give it a ⭐ on GitHub!

---

**Built with 💙 for the crypto community**

🚀 **NOVA** - Crypto Intelligence System
