# 🗂️ Project Reorganization Plan

## Current Issues
- ❌ Too many files in root directory
- ❌ Scattered documentation
- ❌ Duplicate/overlapping folders
- ❌ Shell scripts everywhere
- ❌ Unclear structure for new users

## New Structure

```
Kraken_Cloud_ML_Strat/
│
├── 📱 app.py                          # Main Streamlit dashboard
├── 📋 requirements.txt                # Python dependencies
├── 📖 README.md                       # Main documentation
├── 📄 LICENSE
├── ⚙️  .gitignore
│
├── 🚀 bin/                            # User-facing scripts
│   ├── train_now.sh                   # Quick training launcher
│   ├── check_training.sh              # Check training status
│   ├── quick-start.sh                 # First-time setup
│   └── dev-setup.sh                   # Development setup
│
├── ⚙️  config/                        # All configuration
│   ├── config.yaml                    # App configuration
│   ├── gcp_config.yaml               # GCP settings
│   ├── rebalancing_config.json       # Portfolio config
│   ├── secrets.yaml.example          # Template
│   └── keys/                         # Service account keys
│       ├── .gitkeep
│       └── (*.json - gitignored)
│
├── 🎨 assets/                         # Static assets
│   ├── icons/
│   ├── images/
│   └── styles/
│
├── 📊 data/                           # Data layer
│   ├── __init__.py
│   ├── kraken_api.py                 # Public API client
│   └── kraken_auth.py                # Private API client
│
├── 🧠 ml/                             # Machine learning
│   ├── __init__.py
│   ├── prediction_service.py         # Main prediction service
│   ├── hybrid_prediction_service.py  # Hybrid predictions
│   ├── lstm_model.py                 # LSTM architecture
│   ├── feature_engineering.py        # Feature creation
│   ├── historical_data_fetcher.py    # Data fetching
│   └── portfolio_rebalancer.py       # Rebalancing logic
│
├── ☁️  gcp/                           # Google Cloud Platform
│   ├── README.md                     # GCP overview
│   ├── training/                     # Training containers
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── training_job.py
│   ├── deployment/                   # Deployment code
│   │   ├── vertex_prediction_service.py
│   │   └── test_endpoint.py
│   └── scripts/                      # GCP automation
│       ├── setup/                    # One-time setup
│       │   ├── enable_apis.sh
│       │   ├── setup_iam.sh
│       │   ├── setup_storage.sh
│       │   └── setup_bigquery.sh
│       ├── training/                 # Training scripts
│       │   ├── deploy_budget_training.sh
│       │   └── deploy_vertex_training.sh
│       └── deployment/               # Endpoint deployment
│           ├── deploy_budget_endpoint.sh
│           └── deploy_vertex_endpoint.sh
│
├── 🧪 tests/                          # All tests
│   ├── unit/
│   │   ├── test_kraken_api.py
│   │   ├── test_prediction.py
│   │   └── test_features.py
│   └── integration/
│       ├── test_gcp.py
│       └── run_backtest.py
│
├── 📚 docs/                           # Documentation
│   ├── README.md                     # Docs index
│   ├── quickstart/
│   │   ├── QUICKSTART.md
│   │   └── TRAIN_ML_MODELS.md       # ← Move here
│   ├── user-guides/
│   │   ├── USER_GUIDE.md
│   │   └── UI_IMPROVEMENTS.md       # ← Move here
│   ├── deployment/
│   │   ├── GCP_ML_SETUP_GUIDE.md
│   │   └── CLOUD_SETUP.md
│   ├── technical/
│   │   ├── TECHNICAL_ARCHITECTURE.md
│   │   └── ML_DEVELOPMENT.md
│   └── changelogs/
│       └── CHANGELOG.md
│
├── 📦 models/                         # Trained models
│   ├── .gitkeep
│   └── (*.h5, *.pkl - gitignored)
│
├── 📁 archive/                        # Old/backup files
│   ├── backup/
│   └── old_scripts/
│
└── 🔧 .github/                        # GitHub config
    └── workflows/
        └── ci.yml

## Files to Delete
- ❌ ROOT_STRUCTURE.md (outdated)
- ❌ PROJECT_INDEX.md (outdated)
- ❌ scripts/ (consolidate into gcp/scripts/)
- ❌ deployment/ (consolidate into gcp/)
- ❌ infrastructure/ (mostly empty)
- ❌ tools/ (mostly empty)
- ❌ cloud_functions/ (move if needed)
- ❌ examples/ (move to docs/examples/)

## Files to Move
- train_now.sh → bin/
- check_training.sh → bin/
- quick-start.sh → bin/
- dev-setup.sh → bin/
- TRAIN_ML_MODELS.md → docs/quickstart/
- UI_IMPROVEMENTS.md → docs/user-guides/
- CHANGELOG.md → docs/changelogs/

## Benefits
✅ Clean root directory
✅ Clear folder purposes
✅ Easy to find things
✅ Professional structure
✅ Better for new contributors
✅ Scalable architecture

