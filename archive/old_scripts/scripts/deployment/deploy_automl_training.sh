#!/bin/bash

# Deploy AutoML Time Series Training
# No TensorFlow needed - Google handles everything!

set -e

PROJECT_ID="crypto-ml-trading-487"
REGION="us-central1"
DATASET_ID="crypto_data"

echo "◈ Deploying AutoML Time Series Training"
echo "◊ No TensorFlow needed - Google Cloud handles everything!"
echo ""

# Set the project
gcloud config set project $PROJECT_ID

# Create AutoML dataset
echo "◉ Creating AutoML Time Series dataset..."
DATASET_NAME="crypto_predictions_$(date +%Y%m%d_%H%M%S)"

# Create dataset
gcloud ai datasets create \
    --display-name="$DATASET_NAME" \
    --region=$REGION \
    --metadata-file=/tmp/dataset_metadata.json

# Create dataset metadata
cat > /tmp/dataset_metadata.json << EOF
{
  "time_series_dataset_metadata": {
    "time_column": "timestamp",
    "time_series_identifier_column": "symbol",
    "target_column": "close",
    "unavailable_at_forecast_columns": [],
    "forecast_horizon": 7,
    "data_granularity": {
      "unit": "DAY",
      "quantity": 1
    },
    "preferred_column_spec": {
      "column_id": "close",
      "data_type": "NUMERIC"
    }
  }
}
EOF

echo "◊ AutoML dataset created: $DATASET_NAME"

# Import data from BigQuery
echo "◉ Importing data from BigQuery..."
IMPORT_OPERATION=$(gcloud ai datasets import \
    --dataset="$DATASET_NAME" \
    --region=$REGION \
    --bigquery-source="bq://$PROJECT_ID.$DATASET_ID.historical_prices" \
    --format="value(name)")

echo "◊ Data import started: $IMPORT_OPERATION"

# Create training job
echo "◉ Creating AutoML training job..."
TRAINING_JOB_NAME="crypto_automl_training_$(date +%Y%m%d_%H%M%S)"

gcloud ai models create \
    --region=$REGION \
    --display-name="$TRAINING_JOB_NAME" \
    --dataset="$DATASET_NAME" \
    --training-pipeline-display-name="$TRAINING_JOB_NAME" \
    --target-column="close" \
    --optimization-objective="MINIMIZE_RMSE"

echo "◊ AutoML training job created: $TRAINING_JOB_NAME"

echo ""
echo "◈ AutoML Training Setup Complete!"
echo ""
echo "◊ Benefits of AutoML:"
echo "  ✅ No TensorFlow installation needed"
echo "  ✅ Google handles model architecture"
echo "  ✅ Automatic hyperparameter tuning"
echo "  ✅ Built-in feature engineering"
echo "  ✅ Automatic model selection"
echo ""
echo "◊ Next steps:"
echo "  1. Wait for training to complete (30-60 minutes)"
echo "  2. Check training status in Vertex AI console"
echo "  3. Deploy model to endpoint"
echo "  4. Use predictions in your app"
echo ""
echo "◊ Monitor training:"
echo "  gcloud ai models list --region=$REGION"
echo "  gcloud ai models describe $TRAINING_JOB_NAME --region=$REGION"
echo ""
echo "◈ AutoML deployment complete! 🚀"
