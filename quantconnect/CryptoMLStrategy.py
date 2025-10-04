# region imports
from AlgorithmImports import *
# endregion

class CryptoMLStrategy(QCAlgorithm):
    """
    Crypto ML Trading Strategy for QuantConnect
    
    Strategy:
    - Uses LSTM predictions to determine weekly rebalancing
    - Trades 4-6 major cryptocurrencies (BTC, ETH, SOL, ADA)
    - Equal-weight baseline with ML-enhanced adjustments
    - Rebalances weekly (Sunday 10 PM CDT)
    
    Risk Management:
    - Max 40% position size per asset
    - Min 10% position size (maintain diversification)
    - Kraken fee model (0.16% maker, 0.26% taker)
    """
    
    def Initialize(self):
        """Initialize algorithm parameters and data."""
        # Set strategy parameters
        self.SetStartDate(2022, 1, 1)  # 3+ years for backtesting
        self.SetEndDate(2025, 10, 4)    # Today
        self.SetCash(5000)              # Starting capital
        
        # Set brokerage model
        self.SetBrokerageModel(BrokerageName.Kraken, AccountType.Cash)
        
        # Add cryptocurrencies
        self.symbols = {}
        self.symbols['BTC'] = self.AddCrypto("BTCUSD", Resolution.Hour).Symbol
        self.symbols['ETH'] = self.AddCrypto("ETHUSD", Resolution.Hour).Symbol
        self.symbols['SOL'] = self.AddCrypto("SOLUSD", Resolution.Hour).Symbol
        self.symbols['ADA'] = self.AddCrypto("ADAUSD", Resolution.Hour).Symbol
        
        # Set benchmark to BTC
        self.SetBenchmark(self.symbols['BTC'])
        
        # Risk management parameters
        self.max_position_size = 0.40  # 40% max
        self.min_position_size = 0.10  # 10% min
        self.min_trade_value = 50      # $50 minimum trade
        
        # Rebalancing schedule: Weekly on Sunday at 10 PM CDT
        self.Schedule.On(
            self.DateRules.Every(DayOfWeek.Sunday),
            self.TimeRules.At(22, 0),  # 10 PM
            self.Rebalance
        )
        
        # Store predictions (will be loaded from external source)
        self.predictions = {}
        
        # Performance tracking
        self.last_rebalance = None
        self.rebalance_count = 0
        
        self.Debug(f"✅ Initialized Crypto ML Strategy")
        self.Debug(f"   Trading: {', '.join(self.symbols.keys())}")
        self.Debug(f"   Starting Capital: ${self.Portfolio.Cash:,.2f}")
    
    def OnData(self, data):
        """
        Process incoming data. Main logic is in scheduled Rebalance().
        This is just for monitoring.
        """
        # Monitor for data issues
        for symbol_name, symbol in self.symbols.items():
            if not data.ContainsKey(symbol):
                continue
                
            if data[symbol] is None:
                self.Debug(f"⚠️  No data for {symbol_name}")
    
    def Rebalance(self):
        """
        Weekly rebalancing logic.
        
        In production, this will:
        1. Load ML predictions from external source
        2. Calculate target allocation based on predictions
        3. Apply risk constraints
        4. Execute trades
        """
        self.rebalance_count += 1
        self.Debug(f"\n{'='*60}")
        self.Debug(f"🔄 Rebalance #{self.rebalance_count} - {self.Time}")
        self.Debug(f"{'='*60}")
        
        # Get current portfolio value
        portfolio_value = self.Portfolio.TotalPortfolioValue
        self.Debug(f"💰 Portfolio Value: ${portfolio_value:,.2f}")
        
        # Calculate target allocations
        # For now: Equal weight (25% each)
        # TODO: Replace with ML predictions
        target_allocations = self.GetTargetAllocations()
        
        # Display targets
        self.Debug("\n📊 Target Allocations:")
        for symbol_name, weight in target_allocations.items():
            self.Debug(f"   {symbol_name}: {weight*100:.1f}%")
        
        # Execute rebalancing
        for symbol_name, target_weight in target_allocations.items():
            symbol = self.symbols[symbol_name]
            
            # Skip if no data
            if not self.Securities[symbol].HasData:
                self.Debug(f"⚠️  Skipping {symbol_name} - no data")
                continue
            
            # Calculate target quantity
            target_value = portfolio_value * target_weight
            current_price = self.Securities[symbol].Price
            
            if current_price == 0:
                self.Debug(f"⚠️  Skipping {symbol_name} - price is 0")
                continue
            
            target_quantity = target_value / current_price
            current_quantity = self.Portfolio[symbol].Quantity
            
            # Calculate trade needed
            quantity_diff = target_quantity - current_quantity
            trade_value = abs(quantity_diff * current_price)
            
            # Skip small trades
            if trade_value < self.min_trade_value:
                self.Debug(f"   {symbol_name}: No trade (${trade_value:.2f} < min)")
                continue
            
            # Execute trade
            if quantity_diff > 0:
                self.MarketOrder(symbol, quantity_diff)
                self.Debug(f"   ✅ BUY {quantity_diff:.6f} {symbol_name} @ ${current_price:,.2f}")
            elif quantity_diff < 0:
                self.MarketOrder(symbol, quantity_diff)
                self.Debug(f"   ✅ SELL {abs(quantity_diff):.6f} {symbol_name} @ ${current_price:,.2f}")
        
        # Log current holdings
        self.LogHoldings()
        
        self.last_rebalance = self.Time
    
    def GetTargetAllocations(self):
        """
        Calculate target portfolio allocations.
        
        Current: Equal weight (baseline strategy)
        Future: ML-enhanced weights based on predictions
        """
        # Equal weight baseline
        num_assets = len(self.symbols)
        equal_weight = 1.0 / num_assets
        
        allocations = {symbol_name: equal_weight for symbol_name in self.symbols.keys()}
        
        # TODO: Integrate ML predictions
        # if self.predictions:
        #     allocations = self.ApplyMLPredictions(allocations)
        
        # Apply risk constraints
        for symbol_name in allocations:
            allocations[symbol_name] = max(
                self.min_position_size,
                min(self.max_position_size, allocations[symbol_name])
            )
        
        # Normalize to sum to 1.0
        total = sum(allocations.values())
        allocations = {k: v/total for k, v in allocations.items()}
        
        return allocations
    
    def LogHoldings(self):
        """Log current portfolio holdings."""
        self.Debug("\n📋 Current Holdings:")
        
        total_value = self.Portfolio.TotalPortfolioValue
        
        for symbol_name, symbol in self.symbols.items():
            holding = self.Portfolio[symbol]
            
            if holding.Quantity == 0:
                continue
            
            value = holding.HoldingsValue
            percentage = (value / total_value) * 100 if total_value > 0 else 0
            unrealized_pnl = holding.UnrealizedProfit
            
            self.Debug(f"   {symbol_name}: {holding.Quantity:.6f} | "
                      f"${value:,.2f} ({percentage:.1f}%) | "
                      f"P&L: ${unrealized_pnl:+,.2f}")
        
        cash = self.Portfolio.Cash
        cash_pct = (cash / total_value) * 100 if total_value > 0 else 0
        self.Debug(f"   CASH: ${cash:,.2f} ({cash_pct:.1f}%)")
    
    def OnEndOfAlgorithm(self):
        """Summary statistics at end of backtest."""
        self.Debug(f"\n{'='*60}")
        self.Debug(f"📊 BACKTEST COMPLETE")
        self.Debug(f"{'='*60}")
        self.Debug(f"Starting Value: ${5000:,.2f}")
        self.Debug(f"Ending Value: ${self.Portfolio.TotalPortfolioValue:,.2f}")
        
        total_return = ((self.Portfolio.TotalPortfolioValue - 5000) / 5000) * 100
        self.Debug(f"Total Return: {total_return:+.2f}%")
        self.Debug(f"Rebalances: {self.rebalance_count}")
        
        self.LogHoldings()
        
        self.Debug("\n💡 Next Steps:")
        self.Debug("   1. Integrate ML predictions")
        self.Debug("   2. Add more sophisticated risk management")
        self.Debug("   3. Optimize rebalancing frequency")
        self.Debug("   4. Compare vs buy-and-hold benchmark")

