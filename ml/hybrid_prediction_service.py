#!/usr/bin/env python3
"""
Hybrid Prediction Service
Combines enhanced mock predictions with real ML models for the best of both worlds
"""

import os
import logging
from typing import Dict, List, Optional
from datetime import datetime

from ml.prediction_service import PredictionService
try:
    from gcp.deployment.vertex_prediction_service import VertexPredictionService
except ImportError:
    VertexPredictionService = None

logger = logging.getLogger(__name__)

class HybridPredictionService:
    """
    Hybrid prediction service that combines:
    1. Real ML models (when available)
    2. Enhanced mock predictions (always available)
    3. Basic mock predictions (fallback)
    """
    
    def __init__(self, models_dir: str = "models"):
        """
        Initialize hybrid prediction service
        
        Args:
            models_dir: Directory for local model storage
        """
        self.models_dir = models_dir
        self.models_status = {}
        
        # Initialize components
        self.enhanced_service = PredictionService(provider="local", models_dir=models_dir)
        self.vertex_service = None
        self.local_ml_models = {}
        
        # Initialize Vertex AI service if available
        self._init_vertex_ai()
        
        # Initialize local ML models if available
        self._init_local_ml_models()
        
        logger.info("🔀 Hybrid Prediction Service initialized")
        logger.info(f"   Enhanced Mock: ✅ Available")
        logger.info(f"   Vertex AI: {'✅ Available' if self.vertex_service else '❌ Not available'}")
        logger.info(f"   Local ML Models: {'✅ Available' if self.local_ml_models else '❌ Not available'}")
    
    def _init_vertex_ai(self):
        """Initialize Vertex AI prediction service"""
        try:
            if VertexPredictionService is None:
                logger.warning("◊ Vertex AI service not available - dependencies missing")
                return
                
            project_id = os.getenv('GOOGLE_CLOUD_PROJECT', 'crypto-ml-trading-487')
            region = os.getenv('GCP_REGION', 'us-central1')
            endpoint_id = os.getenv('VERTEX_ENDPOINT_ID', '1074806701011501056')
            
            if endpoint_id:
                self.vertex_service = VertexPredictionService(
                    project_id=project_id,
                    region=region,
                    endpoint_id=endpoint_id
                )
                logger.info("◊ Vertex AI service initialized")
            else:
                logger.warning("◊ Vertex AI endpoint ID not configured")
                
        except Exception as e:
            logger.warning(f"◊ Vertex AI initialization failed: {e}")
    
    def _init_local_ml_models(self):
        """Initialize local ML models if available"""
        try:
            # Check if we have trained models in the models directory
            if os.path.exists(self.models_dir):
                model_files = [f for f in os.listdir(self.models_dir) if f.endswith('.h5')]
                
                for model_file in model_files:
                    symbol = model_file.replace('lstm_model_', '').replace('.h5', '').upper()
                    model_path = os.path.join(self.models_dir, model_file)
                    
                    # For now, just track that we have the model
                    # In a real implementation, you'd load the model here
                    self.local_ml_models[symbol] = {
                        'path': model_path,
                        'type': 'lstm',
                        'loaded': False  # Would be True if we actually loaded it
                    }
                    
                if self.local_ml_models:
                    logger.info(f"◊ Found {len(self.local_ml_models)} local ML models")
                    
        except Exception as e:
            logger.warning(f"◊ Local ML model initialization failed: {e}")
    
    def get_prediction(self, symbol: str, days_ahead: int = 7) -> Dict:
        """
        Get prediction using hybrid approach
        
        Priority order:
        1. Real ML model (Vertex AI or local)
        2. Enhanced mock prediction
        3. Basic mock prediction (fallback)
        
        Args:
            symbol: Cryptocurrency symbol (e.g., 'BTC')
            days_ahead: Number of days to predict ahead
            
        Returns:
            Dictionary with prediction data
        """
        logger.info(f"🔀 Getting hybrid prediction for {symbol} ({days_ahead} days ahead)")
        
        # Try real ML model first (Vertex AI)
        if self.vertex_service:
            try:
                logger.info(f"   Trying Vertex AI for {symbol}...")
                ml_prediction = self.vertex_service.get_prediction(symbol, days_ahead)
                
                if ml_prediction and ml_prediction.get('status') == 'success':
                    ml_prediction['prediction_source'] = 'vertex_ai_ml'
                    ml_prediction['prediction_type'] = 'real_ml'
                    logger.info(f"   ✅ Using Vertex AI ML prediction for {symbol}")
                    return ml_prediction
                else:
                    logger.info(f"   ⚠️ Vertex AI failed for {symbol}, falling back")
                    
            except Exception as e:
                logger.warning(f"   ⚠️ Vertex AI error for {symbol}: {e}")
        
        # Try local ML model
        if symbol in self.local_ml_models:
            try:
                logger.info(f"   Trying local ML model for {symbol}...")
                local_prediction = self._predict_with_local_model(symbol, days_ahead)
                
                if local_prediction:
                    local_prediction['prediction_source'] = 'local_ml'
                    local_prediction['prediction_type'] = 'real_ml'
                    logger.info(f"   ✅ Using local ML prediction for {symbol}")
                    return local_prediction
                else:
                    logger.info(f"   ⚠️ Local ML failed for {symbol}, falling back")
                    
            except Exception as e:
                logger.warning(f"   ⚠️ Local ML error for {symbol}: {e}")
        
        # Fall back to enhanced mock prediction
        try:
            logger.info(f"   Using enhanced mock prediction for {symbol}...")
            enhanced_prediction = self.enhanced_service.get_prediction(symbol, days_ahead)
            enhanced_prediction['prediction_source'] = 'enhanced_mock'
            enhanced_prediction['prediction_type'] = 'enhanced_mock'
            logger.info(f"   ✅ Using enhanced mock prediction for {symbol}")
            return enhanced_prediction
            
        except Exception as e:
            logger.warning(f"   ⚠️ Enhanced mock error for {symbol}: {e}")
            
            # Final fallback to basic mock
            basic_prediction = self._get_basic_mock_prediction(symbol, days_ahead)
            basic_prediction['prediction_source'] = 'basic_mock'
            basic_prediction['prediction_type'] = 'basic_mock'
            logger.warning(f"   ⚠️ Using basic mock prediction for {symbol}")
            return basic_prediction
    
    def _predict_with_local_model(self, symbol: str, days_ahead: int) -> Optional[Dict]:
        """Predict using local ML model"""
        # This is a placeholder for actual ML model prediction
        # In a real implementation, you would:
        # 1. Load the model
        # 2. Prepare input features
        # 3. Make prediction
        # 4. Return formatted result
        
        return None  # For now, return None to trigger fallback
    
    def _get_basic_mock_prediction(self, symbol: str, days_ahead: int) -> Dict:
        """Get basic mock prediction as final fallback"""
        import random
        import numpy as np
        
        # Basic mock prediction
        current_price = 45000 if symbol == 'BTC' else 3000 if symbol == 'ETH' else 100
        
        # Random prediction
        np.random.seed(hash(symbol + str(days_ahead)) % 2**32)
        return_change = np.random.normal(0.02, 0.1)  # 2% mean return, 10% volatility
        
        predicted_price = current_price * (1 + return_change)
        
        return {
            'symbol': symbol,
            'current_price': current_price,
            'predicted_price': predicted_price,
            'predicted_return': return_change,
            'confidence': 0.5,
            'days_ahead': days_ahead,
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'prediction_source': 'basic_mock',
            'prediction_type': 'basic_mock'
        }
    
    def get_all_predictions(self, symbols: List[str], days_ahead: int = 7) -> Dict[str, Dict]:
        """
        Get predictions for all symbols using hybrid approach
        
        Args:
            symbols: List of cryptocurrency symbols
            days_ahead: Number of days to predict ahead
            
        Returns:
            Dictionary mapping symbols to their predictions
        """
        logger.info(f"🔀 Getting hybrid predictions for {len(symbols)} symbols")
        
        predictions = {}
        source_counts = {'real_ml': 0, 'enhanced_mock': 0, 'basic_mock': 0}
        
        for symbol in symbols:
            prediction = self.get_prediction(symbol, days_ahead)
            predictions[symbol] = prediction
            
            # Count prediction sources
            prediction_type = prediction.get('prediction_type', 'basic_mock')
            source_counts[prediction_type] += 1
        
        logger.info(f"✅ Generated {len(predictions)} predictions")
        logger.info(f"   Real ML: {source_counts['real_ml']}")
        logger.info(f"   Enhanced Mock: {source_counts['enhanced_mock']}")
        logger.info(f"   Basic Mock: {source_counts['basic_mock']}")
        
        return predictions
    
    def _has_model(self, symbol: str) -> bool:
        """Check if trained model exists for symbol."""
        # Check local ML models first
        if symbol in self.local_ml_models:
            return True
        
        # Check if model file exists in models directory
        import os
        model_path = os.path.join(self.models_dir, f"{symbol}_model.h5")
        return os.path.exists(model_path)
    
    def train_model(self, symbol: str, days: int = 365, epochs: int = 50, save_model: bool = True) -> Dict:
        """Train model for a specific symbol using the enhanced service."""
        try:
            return self.enhanced_service.train_model(symbol, days, epochs, save_model)
        except Exception as e:
            logger.error(f"Training failed for {symbol}: {e}")
            return {
                'status': 'error',
                'message': f'Training failed: {e}',
                'symbol': symbol
            }
    
    def train_all_models(self, days: int = 365, epochs: int = 50) -> Dict:
        """Train models for all supported symbols using the enhanced service."""
        try:
            return self.enhanced_service.train_all_models(days, epochs)
        except Exception as e:
            logger.error(f"Training all models failed: {e}")
            return {
                'status': 'error',
                'message': f'Training failed: {e}',
                'results': {}
            }
    
    def get_prediction_summary(self) -> Dict:
        """Get summary of prediction system status"""
        return {
            'enhanced_mock_available': True,
            'vertex_ai_available': self.vertex_service is not None,
            'local_ml_models_available': len(self.local_ml_models) > 0,
            'local_ml_models_count': len(self.local_ml_models),
            'supported_symbols': list(self.local_ml_models.keys()) + ['BTC', 'ETH', 'SOL', 'ADA', 'DOT', 'XRP'],
            'system_status': 'hybrid_operational'
        }
