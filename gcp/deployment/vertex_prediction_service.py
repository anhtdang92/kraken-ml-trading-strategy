#!/usr/bin/env python3
"""
Vertex AI Prediction Service
This service handles predictions using Vertex AI endpoints
"""

import os
import json
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta

import pandas as pd
import numpy as np
from google.cloud import aiplatform
from google.cloud import bigquery
from google.cloud import storage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VertexPredictionService:
    """Vertex AI prediction service for crypto price predictions"""
    
    def __init__(self, project_id: str, region: str, endpoint_id: str):
        self.project_id = project_id
        self.region = region
        self.endpoint_id = endpoint_id
        
        # Initialize clients
        self.bq_client = bigquery.Client(project=project_id)
        self.storage_client = storage.Client(project=project_id)
        
        # Initialize Vertex AI
        aiplatform.init(project=project_id, location=region)
        
        # Get endpoint
        self.endpoint = aiplatform.Endpoint(endpoint_id)
        
        logger.info(f"◈ Initialized Vertex AI prediction service")
        logger.info(f"◊ Project: {project_id}")
        logger.info(f"◊ Region: {region}")
        logger.info(f"◊ Endpoint: {endpoint_id}")
    
    def get_latest_data(self, symbol: str, lookback_days: int = 7) -> pd.DataFrame:
        """Get latest data for a symbol from BigQuery"""
        query = f"""
        SELECT 
            timestamp,
            open, high, low, close, volume
        FROM `{self.project_id}.crypto_data.historical_prices`
        WHERE symbol = '{symbol}'
        ORDER BY timestamp DESC
        LIMIT {lookback_days}
        """
        
        df = self.bq_client.query(query).to_dataframe()
        if len(df) == 0:
            raise ValueError(f"No data found for symbol: {symbol}")
        
        # Sort by timestamp ascending
        df = df.sort_values('timestamp').reset_index(drop=True)
        
        logger.info(f"◊ Fetched {len(df)} records for {symbol}")
        return df
    
    def prepare_features(self, df: pd.DataFrame) -> np.ndarray:
        """Prepare features for prediction"""
        from ml.feature_engineering import FeatureEngineer
        
        # Add technical indicators
        feature_engineer = FeatureEngineer()
        df_with_features = feature_engineer.add_all_features(df)
        
        # Select feature columns
        feature_columns = [
            'open', 'high', 'low', 'close', 'volume',
            'ma_7', 'ma_14', 'ma_30', 'rsi', 'volume_momentum',
            'price_momentum', 'volatility'
        ]
        
        # Get the last sequence
        features = df_with_features[feature_columns].values
        
        # Reshape for LSTM input (1, sequence_length, features)
        features = features.reshape(1, features.shape[0], features.shape[1])
        
        return features
    
    def predict_single(self, symbol: str, lookback_days: int = 7) -> Dict:
        """Make a single prediction for a symbol"""
        try:
            # Get latest data
            df = self.get_latest_data(symbol, lookback_days)
            
            # Prepare features
            features = self.prepare_features(df)
            
            # Make prediction
            prediction = self.endpoint.predict(
                instances=[features.tolist()],
                parameters={"confidence_threshold": 0.5}
            )
            
            # Extract results
            predictions = prediction.predictions[0]
            predicted_price = predictions[0]
            confidence = predictions[1] if len(predictions) > 1 else 0.8
            
            # Calculate current price
            current_price = df['close'].iloc[-1]
            
            # Calculate percentage change
            price_change = (predicted_price - current_price) / current_price * 100
            
            result = {
                'symbol': symbol,
                'current_price': float(current_price),
                'predicted_price': float(predicted_price),
                'price_change': float(price_change),
                'confidence': float(confidence),
                'timestamp': datetime.now(),
                'model_version': 'vertex-ai-v1'
            }
            
            logger.info(f"◊ Prediction for {symbol}: ${current_price:.2f} → ${predicted_price:.2f} ({price_change:+.2f}%)")
            
            return result
            
        except Exception as e:
            logger.error(f"◊ Prediction failed for {symbol}: {str(e)}")
            return {
                'symbol': symbol,
                'error': str(e),
                'timestamp': datetime.now()
            }
    
    def predict_all(self, symbols: List[str]) -> List[Dict]:
        """Make predictions for all symbols"""
        logger.info(f"◈ Making predictions for {len(symbols)} symbols...")
        
        predictions = []
        for symbol in symbols:
            prediction = self.predict_single(symbol)
            predictions.append(prediction)
        
        # Log predictions to BigQuery
        self.log_predictions(predictions)
        
        return predictions
    
    def log_predictions(self, predictions: List[Dict]):
        """Log predictions to BigQuery"""
        logger.info("◊ Logging predictions to BigQuery...")
        
        # Prepare data for BigQuery
        bq_data = []
        for pred in predictions:
            if 'error' not in pred:
                bq_data.append({
                    'timestamp': pred['timestamp'],
                    'symbol': pred['symbol'],
                    'predicted_price': pred['predicted_price'],
                    'confidence': pred['confidence'],
                    'model_version': pred['model_version'],
                    'created_at': datetime.now()
                })
        
        if bq_data:
            # Insert into BigQuery
            table_id = f"{self.project_id}.crypto_data.predictions"
            self.bq_client.insert_rows_json(table_id, bq_data)
            
            logger.info(f"◊ Logged {len(bq_data)} predictions to BigQuery")
    
    def get_endpoint_info(self) -> Dict:
        """Get endpoint information"""
        return {
            'endpoint_id': self.endpoint_id,
            'project_id': self.project_id,
            'region': self.region,
            'endpoint_name': self.endpoint.display_name,
            'deployed_models': len(self.endpoint.list_models()),
            'status': 'active'
        }

def main():
    """Test the Vertex AI prediction service"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Test Vertex AI Prediction Service')
    parser.add_argument('--project_id', required=True, help='GCP Project ID')
    parser.add_argument('--region', required=True, help='GCP Region')
    parser.add_argument('--endpoint_id', required=True, help='Vertex AI Endpoint ID')
    parser.add_argument('--symbols', required=True, help='Comma-separated list of symbols')
    
    args = parser.parse_args()
    
    # Initialize service
    service = VertexPredictionService(
        project_id=args.project_id,
        region=args.region,
        endpoint_id=args.endpoint_id
    )
    
    # Test predictions
    symbols = args.symbols.split(',')
    predictions = service.predict_all(symbols)
    
    # Print results
    print("\n◈ Prediction Results:")
    for pred in predictions:
        if 'error' not in pred:
            print(f"◊ {pred['symbol']}: ${pred['current_price']:.2f} → ${pred['predicted_price']:.2f} ({pred['price_change']:+.2f}%)")
        else:
            print(f"◊ {pred['symbol']}: Error - {pred['error']}")

if __name__ == "__main__":
    main()
