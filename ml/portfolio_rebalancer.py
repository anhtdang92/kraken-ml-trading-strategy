"""
Portfolio Rebalancer for Crypto ML Trading Dashboard

This service handles portfolio rebalancing logic:
- Calculates target allocations based on ML predictions
- Implements risk controls and position limits
- Generates buy/sell orders with fee calculations
- Handles paper trading vs live trading modes

Architecture:
    Strategy: Equal-weight base + ML enhancement
    Risk Controls: Position limits, trade size minimums
    Execution: Paper trading first, then live trading
    Schedule: Weekly rebalancing (configurable)

Usage:
    # Initialize rebalancer
    rebalancer = PortfolioRebalancer()
    
    # Get rebalancing recommendations
    recommendations = rebalancer.get_rebalancing_recommendations()
    
    # Execute rebalancing (paper trading)
    results = rebalancer.execute_rebalancing(paper_trading=True)
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import json
from pathlib import Path

# Local imports
from .prediction_service import PredictionService
from data.kraken_api import KrakenAPI

logger = logging.getLogger(__name__)


class PortfolioRebalancer:
    """
    Portfolio rebalancing service with ML-enhanced allocation strategy.
    
    This service implements:
    1. Base Strategy: Equal-weight allocation across cryptocurrencies
    2. ML Enhancement: Adjust weights based on predicted returns
    3. Risk Controls: Position limits and trade size minimums
    4. Execution: Paper trading and live trading modes
    """
    
    # Configuration
    SUPPORTED_SYMBOLS = ['BTC', 'ETH', 'SOL', 'ADA', 'DOT', 'XRP']
    BASE_ALLOCATION = 1.0 / len(SUPPORTED_SYMBOLS)  # Equal weight (16.67% each)
    
    # Risk controls
    MAX_POSITION_WEIGHT = 0.40  # Max 40% per position
    MIN_POSITION_WEIGHT = 0.10  # Min 10% per position
    MIN_TRADE_SIZE = 50.0       # Min $50 trade size
    TRADING_FEE = 0.0016       # Kraken maker fee (0.16%)
    
    # ML enhancement parameters
    ML_WEIGHT_FACTOR = 0.3     # How much ML predictions affect allocation
    CONFIDENCE_THRESHOLD = 0.6  # Min confidence for ML adjustment
    
    def __init__(self, paper_trading: bool = True, config_file: str = "config/rebalancing_config.json"):
        """
        Initialize the portfolio rebalancer.
        
        Args:
            paper_trading: If True, use paper trading mode (no real trades)
            config_file: Path to configuration file
        """
        self.paper_trading = paper_trading
        self.config_file = config_file
        self.prediction_service = PredictionService()
        self.kraken_api = KrakenAPI()
        
        # Portfolio state
        self.current_portfolio = {}
        self.target_portfolio = {}
        self.rebalancing_orders = []
        
        # Load configuration
        self.config = self._load_config()
        
        logger.info(f"🔄 Portfolio Rebalancer initialized (Paper Trading: {paper_trading})")
    
    def _load_config(self) -> Dict:
        """Load configuration from file."""
        default_config = {
            "max_position_weight": self.MAX_POSITION_WEIGHT,
            "min_position_weight": self.MIN_POSITION_WEIGHT,
            "min_trade_size": self.MIN_TRADE_SIZE,
            "trading_fee": self.TRADING_FEE,
            "ml_weight_factor": self.ML_WEIGHT_FACTOR,
            "confidence_threshold": self.CONFIDENCE_THRESHOLD,
            "rebalancing_schedule": "weekly",
            "last_rebalancing": None
        }
        
        try:
            config_path = Path(self.config_file)
            if config_path.exists():
                with open(config_path, 'r') as f:
                    loaded_config = json.load(f)
                # Merge with defaults
                default_config.update(loaded_config)
            else:
                # Create default config file
                config_path.parent.mkdir(parents=True, exist_ok=True)
                with open(config_path, 'w') as f:
                    json.dump(default_config, f, indent=2)
        except Exception as e:
            logger.warning(f"Could not load config: {e}, using defaults")
        
        return default_config
    
    def save_config(self) -> bool:
        """Save current configuration to file."""
        try:
            config_path = Path(self.config_file)
            config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            logger.info("Configuration saved successfully")
            return True
        except Exception as e:
            logger.error(f"Could not save config: {e}")
            return False
    
    def get_current_portfolio(self) -> Dict[str, float]:
        """
        Get current portfolio allocation.
        
        Returns:
            Dict mapping symbol to current weight (0.0 to 1.0)
        """
        # For now, return mock portfolio data
        # In production, this would fetch from Kraken API or database
        mock_portfolio = {
            'BTC': 0.25,   # 25%
            'ETH': 0.20,   # 20%
            'SOL': 0.15,   # 15%
            'ADA': 0.15,   # 15%
            'DOT': 0.15,   # 15%
            'XRP': 0.10,   # 10%
        }
        
        self.current_portfolio = mock_portfolio
        logger.info("📊 Current portfolio retrieved")
        return self.current_portfolio
    
    def get_target_allocation(self, use_ml: bool = True) -> Dict[str, float]:
        """
        Calculate target portfolio allocation.
        
        Args:
            use_ml: If True, use ML predictions to enhance allocation
            
        Returns:
            Dict mapping symbol to target weight (0.0 to 1.0)
        """
        if not use_ml:
            # Equal-weight allocation
            target_allocation = {symbol: self.BASE_ALLOCATION for symbol in self.SUPPORTED_SYMBOLS}
        else:
            # ML-enhanced allocation
            target_allocation = self._calculate_ml_enhanced_allocation()
        
        # Apply risk controls
        target_allocation = self._apply_risk_controls(target_allocation)
        
        self.target_portfolio = target_allocation
        logger.info("Target allocation calculated")
        return self.target_portfolio
    
    def _calculate_ml_enhanced_allocation(self) -> Dict[str, float]:
        """
        Calculate ML-enhanced target allocation.
        
        Returns:
            Dict mapping symbol to target weight
        """
        # Get ML predictions
        predictions = self.prediction_service.get_all_predictions(days_ahead=7)
        
        # Start with equal weights
        base_weights = {symbol: self.BASE_ALLOCATION for symbol in self.SUPPORTED_SYMBOLS}
        
        # Apply ML adjustments
        ml_adjustments = {}
        for pred in predictions:
            symbol = pred['symbol']
            predicted_return = pred['predicted_return']
            confidence = pred['confidence']
            
            # Only apply ML adjustment if confidence is high enough
            if confidence >= self.CONFIDENCE_THRESHOLD:
                # Scale adjustment by confidence and ML weight factor
                adjustment = predicted_return * confidence * self.ML_WEIGHT_FACTOR
                ml_adjustments[symbol] = adjustment
            else:
                ml_adjustments[symbol] = 0.0
        
        # Apply adjustments to base weights
        total_adjustment = sum(ml_adjustments.values())
        if total_adjustment != 0:
            # Normalize adjustments to maintain total weight = 1.0
            for symbol in self.SUPPORTED_SYMBOLS:
                base_weights[symbol] += ml_adjustments.get(symbol, 0.0)
        
        # Ensure weights sum to 1.0
        total_weight = sum(base_weights.values())
        if total_weight > 0:
            base_weights = {k: v/total_weight for k, v in base_weights.items()}
        
        logger.info(f"🧠 ML-enhanced allocation calculated with adjustments: {ml_adjustments}")
        return base_weights
    
    def _apply_risk_controls(self, allocation: Dict[str, float]) -> Dict[str, float]:
        """
        Apply risk controls to target allocation.
        
        Args:
            allocation: Raw target allocation
            
        Returns:
            Risk-controlled allocation
        """
        controlled_allocation = {}
        
        for symbol, weight in allocation.items():
            # Apply position limits
            weight = max(self.MIN_POSITION_WEIGHT, min(weight, self.MAX_POSITION_WEIGHT))
            controlled_allocation[symbol] = weight
        
        # Renormalize to ensure total = 1.0
        total_weight = sum(controlled_allocation.values())
        if total_weight > 0:
            controlled_allocation = {k: v/total_weight for k, v in controlled_allocation.items()}
        
        logger.info("🛡️ Risk controls applied to target allocation")
        return controlled_allocation
    
    def calculate_rebalancing_orders(self, portfolio_value: float = 10000.0) -> List[Dict]:
        """
        Calculate buy/sell orders needed for rebalancing.
        
        Args:
            portfolio_value: Total portfolio value in USD
            
        Returns:
            List of rebalancing orders
        """
        current = self.get_current_portfolio()
        target = self.get_target_allocation(use_ml=True)
        
        orders = []
        
        for symbol in self.SUPPORTED_SYMBOLS:
            current_weight = current.get(symbol, 0.0)
            target_weight = target.get(symbol, 0.0)
            
            # Calculate weight difference
            weight_diff = target_weight - current_weight
            dollar_diff = weight_diff * portfolio_value
            
            # Only create order if difference is significant
            if abs(dollar_diff) >= self.MIN_TRADE_SIZE:
                order_type = "BUY" if dollar_diff > 0 else "SELL"
                order_size = abs(dollar_diff)
                
                # Calculate fees
                fee = order_size * self.TRADING_FEE
                net_amount = order_size - fee
                
                order = {
                    'symbol': symbol,
                    'type': order_type,
                    'amount_usd': order_size,
                    'net_amount_usd': net_amount,
                    'fee_usd': fee,
                    'current_weight': current_weight,
                    'target_weight': target_weight,
                    'weight_change': weight_diff,
                    'timestamp': datetime.now().isoformat()
                }
                
                orders.append(order)
        
        self.rebalancing_orders = orders
        logger.info(f"📋 Generated {len(orders)} rebalancing orders")
        return orders
    
    def get_rebalancing_summary(self) -> Dict:
        """
        Get comprehensive rebalancing summary.
        
        Returns:
            Dict with rebalancing analysis and recommendations
        """
        current = self.get_current_portfolio()
        target = self.get_target_allocation(use_ml=True)
        orders = self.calculate_rebalancing_orders()
        
        # Calculate portfolio metrics
        total_trades = len(orders)
        total_fees = sum(order['fee_usd'] for order in orders)
        buy_orders = [o for o in orders if o['type'] == 'BUY']
        sell_orders = [o for o in orders if o['type'] == 'SELL']
        
        # Calculate allocation drift
        drift_metrics = {}
        for symbol in self.SUPPORTED_SYMBOLS:
            current_weight = current.get(symbol, 0.0)
            target_weight = target.get(symbol, 0.0)
            drift = abs(target_weight - current_weight)
            drift_metrics[symbol] = {
                'current': current_weight,
                'target': target_weight,
                'drift': drift,
                'status': 'OVERWEIGHT' if current_weight > target_weight else 'UNDERWEIGHT'
            }
        
        summary = {
            'timestamp': datetime.now().isoformat(),
            'paper_trading': self.paper_trading,
            'current_allocation': current,
            'target_allocation': target,
            'orders': orders,
            'metrics': {
                'total_trades': total_trades,
                'total_fees': total_fees,
                'buy_orders': len(buy_orders),
                'sell_orders': len(sell_orders),
                'max_drift': max(drift_metrics[s]['drift'] for s in drift_metrics),
                'avg_drift': np.mean([drift_metrics[s]['drift'] for s in drift_metrics])
            },
            'drift_analysis': drift_metrics,
            'recommendations': self._generate_recommendations(drift_metrics, orders)
        }
        
        logger.info("📊 Rebalancing summary generated")
        return summary
    
    def _generate_recommendations(self, drift_analysis: Dict, orders: List[Dict]) -> List[str]:
        """
        Generate rebalancing recommendations.
        
        Args:
            drift_analysis: Analysis of allocation drift
            orders: List of rebalancing orders
            
        Returns:
            List of recommendation strings
        """
        recommendations = []
        
        # Check for significant drift
        max_drift = max(drift_analysis[s]['drift'] for s in drift_analysis)
        if max_drift > 0.05:  # 5% drift threshold
            recommendations.append("⚠️ Significant allocation drift detected - rebalancing recommended")
        
        # Check for high fees
        total_fees = sum(order['fee_usd'] for order in orders)
        if total_fees > 100:  # $100 fee threshold
            recommendations.append("💰 High trading fees - consider batching orders")
        
        # Check for many small trades
        small_trades = [o for o in orders if o['amount_usd'] < 200]
        if len(small_trades) > 3:
            recommendations.append("📦 Many small trades - consider consolidating")
        
        # Check for ML confidence
        if not self.paper_trading:
            recommendations.append("🚨 Live trading mode - review all orders before execution")
        
        if not recommendations:
            recommendations.append("✅ Portfolio is well-balanced - no immediate rebalancing needed")
        
        return recommendations
    
    def execute_rebalancing(self, portfolio_value: float = 10000.0) -> Dict:
        """
        Execute portfolio rebalancing.
        
        Args:
            portfolio_value: Total portfolio value in USD
            
        Returns:
            Dict with execution results
        """
        if self.paper_trading:
            return self._execute_paper_trading(portfolio_value)
        else:
            return self._execute_live_trading(portfolio_value)
    
    def _execute_paper_trading(self, portfolio_value: float) -> Dict:
        """
        Execute paper trading rebalancing.
        
        Args:
            portfolio_value: Total portfolio value in USD
            
        Returns:
            Dict with paper trading results
        """
        orders = self.calculate_rebalancing_orders(portfolio_value)
        
        # Simulate order execution
        executed_orders = []
        for order in orders:
            # Simulate successful execution
            executed_order = order.copy()
            executed_order['status'] = 'EXECUTED'
            executed_order['execution_time'] = datetime.now().isoformat()
            executed_order['paper_trading'] = True
            executed_orders.append(executed_order)
        
        result = {
            'status': 'success',
            'mode': 'paper_trading',
            'orders_executed': len(executed_orders),
            'total_fees': sum(order['fee_usd'] for order in executed_orders),
            'execution_time': datetime.now().isoformat(),
            'orders': executed_orders
        }
        
        logger.info(f"📝 Paper trading executed: {len(executed_orders)} orders")
        return result
    
    def _execute_live_trading(self, portfolio_value: float) -> Dict:
        """
        Execute live trading rebalancing.
        
        Args:
            portfolio_value: Total portfolio value in USD
            
        Returns:
            Dict with live trading results
        """
        # This would integrate with Kraken API for real trading
        # For now, return a placeholder
        return {
            'status': 'error',
            'message': 'Live trading not implemented yet - use paper trading mode',
            'mode': 'live_trading'
        }
