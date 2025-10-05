# GCP ML Infrastructure Setup

This directory contains the Google Cloud Platform infrastructure setup for machine learning predictions using Vertex AI.

## Overview

The GCP setup enables:
- **Vertex AI**: Training and serving LSTM models
- **BigQuery**: Storing historical data and predictions
- **Cloud Storage**: Model artifacts and training data
- **IAM**: Secure service accounts with minimal permissions
- **Cost Optimization**: Preemptible instances, auto-scaling, lifecycle policies

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   Vertex AI    │    │   BigQuery     │
│   Dashboard     │◄──►│   Endpoint     │◄──►│   Data Store   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Cloud Run     │    │   Vertex AI     │    │   Cloud Storage │
│   (App Host)    │    │   Training      │    │   (Models)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Quick Start

### 1. Prerequisites

- Google Cloud SDK installed and authenticated
- Docker installed for container builds
- Python 3.9+ with required dependencies

### 2. One-Command Setup

```bash
# Run the complete setup
bash gcp/scripts/setup_gcp_ml.sh
```

This will:
- Enable all required APIs
- Create service accounts and IAM roles
- Set up BigQuery datasets and tables
- Create Cloud Storage buckets
- Deploy Vertex AI training job
- Deploy prediction endpoint
- Configure the application

### 3. Manual Setup (Step by Step)

If you prefer to run each step individually:

```bash
# 1. Enable APIs
bash gcp/scripts/enable_apis.sh

# 2. Set up IAM
bash gcp/scripts/setup_iam.sh

# 3. Create storage
bash gcp/scripts/setup_storage.sh

# 4. Set up BigQuery
bash gcp/scripts/setup_bigquery.sh

# 5. Deploy training job
bash gcp/scripts/deploy_vertex_training.sh

# 6. Deploy endpoint
bash gcp/scripts/deploy_vertex_endpoint.sh
```

## Configuration

### Environment Variables

The setup creates a `.env` file with:

```bash
GOOGLE_CLOUD_PROJECT=crypto-ml-trading-487
GCP_REGION=us-central1
BIGQUERY_DATASET=crypto_data
STORAGE_BUCKET=crypto-ml-models-487
VERTEX_ENDPOINT_ID=<endpoint_id_after_deployment>
GOOGLE_APPLICATION_CREDENTIALS=config/keys/crypto-app-sa-key.json
```

### Service Accounts

Three service accounts are created with minimal permissions:

- **ml-training-sa**: Vertex AI training jobs
- **ml-prediction-sa**: Vertex AI predictions
- **crypto-app-sa**: Streamlit app access

### BigQuery Schema

Tables created:
- `historical_prices`: OHLCV data from Kraken
- `predictions`: ML model predictions
- `trades`: Trading history
- `model_metrics`: Training performance
- `portfolio_snapshots`: Portfolio state
- `rebalancing_events`: Rebalancing history

## Usage

### Using Vertex AI Predictions

Update your app to use Vertex AI:

```python
from ml.prediction_service import PredictionService

# Initialize with Vertex AI provider
service = PredictionService(provider="vertex")

# Get predictions
predictions = service.get_all_predictions()
```

### Training Models

Models are trained automatically via Vertex AI:

```bash
# Trigger training job
gcloud ai custom-jobs create --region=us-central1 --config=training_job_config.json
```

### Monitoring

Check the status of your infrastructure:

```bash
# View training jobs
gcloud ai custom-jobs list --region=us-central1

# View endpoints
gcloud ai endpoints list --region=us-central1

# Check BigQuery
bq ls crypto-ml-trading-487:crypto_data

# View storage
gsutil ls gs://crypto-ml-models-487/
```

## Cost Optimization

### Budget Controls

- **Target**: $50 credit for 3-4 months
- **Preemptible instances**: 60-80% cost savings
- **Auto-scaling**: Scale to zero when not in use
- **Lifecycle policies**: Auto-delete old data

### Cost Monitoring

Set up billing alerts:
- $10 (20% of budget)
- $25 (50% of budget)  
- $50 (100% of budget)

### Optimization Tips

1. **Use preemptible instances** for training
2. **Scale endpoints to zero** when not in use
3. **Delete old model versions** after 30 days
4. **Use regional persistent disks** (cheaper)
5. **Partition BigQuery tables** by date

## Security

### IAM Permissions

Service accounts have minimal required permissions:
- **ml-training-sa**: Vertex AI + Storage + BigQuery write
- **ml-prediction-sa**: Vertex AI + Storage read
- **crypto-app-sa**: BigQuery read + Storage read + Secret Manager

### Encryption

- All data encrypted at rest
- Service account keys stored securely
- API keys in Secret Manager
- VPC connector for network isolation (optional)

### Key Rotation

- Service account keys rotated every 90 days
- API keys stored in Secret Manager
- Automatic key rotation setup

## Troubleshooting

### Common Issues

1. **Permission denied**: Check service account roles
2. **Training job fails**: Check Docker image and dependencies
3. **Endpoint not responding**: Check endpoint status and logs
4. **High costs**: Review machine types and auto-scaling

### Debug Commands

```bash
# Check training job logs
gcloud ai custom-jobs describe <job_id> --region=us-central1

# Check endpoint status
gcloud ai endpoints describe <endpoint_id> --region=us-central1

# View BigQuery logs
bq query --use_legacy_sql=false "SELECT * FROM \`crypto-ml-trading-487.crypto_data.model_metrics\` ORDER BY timestamp DESC LIMIT 10"
```

### Support

- Check GCP Console for detailed error messages
- Review Cloud Logging for application logs
- Monitor Vertex AI metrics in Cloud Monitoring
- Check BigQuery usage in billing dashboard

## Next Steps

After setup:

1. **Wait for training completion** (check Vertex AI console)
2. **Update endpoint ID** in `.env` file
3. **Test predictions** with sample data
4. **Monitor costs** and performance
5. **Set up alerts** for errors and budget

## Files Structure

```
gcp/
├── scripts/                 # Setup scripts
│   ├── enable_apis.sh      # Enable GCP APIs
│   ├── setup_iam.sh        # IAM roles and service accounts
│   ├── setup_storage.sh    # Cloud Storage buckets
│   ├── setup_bigquery.sh   # BigQuery datasets
│   ├── deploy_vertex_training.sh  # Training job deployment
│   ├── deploy_vertex_endpoint.sh  # Endpoint deployment
│   └── setup_gcp_ml.sh     # Complete setup script
├── training/                # Training job code
│   ├── Dockerfile          # Training container
│   └── vertex_training_job.py  # Training script
├── deployment/              # Deployment code
│   └── vertex_prediction_service.py  # Prediction service
└── README.md               # This file
```

## Cost Breakdown (Estimated)

| Service | Monthly Cost | Notes |
|---------|-------------|-------|
| Vertex AI Training | $5-10 | Preemptible instances |
| Vertex AI Endpoint | $10-20 | Auto-scaling, scale to zero |
| BigQuery | $2-5 | Storage + queries |
| Cloud Storage | $1-2 | Model artifacts |
| Cloud Run | $0 | Free tier |
| **Total** | **$18-37** | **3-4 months on $50** |

This setup provides a production-ready ML infrastructure that can scale with your needs while staying within budget.
