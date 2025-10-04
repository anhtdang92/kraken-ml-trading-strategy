#!/usr/bin/env python3
"""
Local Crypto ML Strategy Backtest
Simulates the QuantConnect strategy locally using historical Kraken data
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys

try:
    from data.kraken_api import KrakenAPI
except ImportError:
    print("❌ Error: Could not import KrakenAPI")
    sys.exit(1)


class LocalBacktest:
    """Simple backtest engine for crypto strategy."""
    
    def __init__(self, initial_capital=5000, symbols=['BTC', 'ETH', 'SOL', 'ADA']):
        """Initialize backtest parameters."""
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.symbols = symbols
        self.holdings = {s: 0.0 for s in symbols}
        self.portfolio_history = []
        self.trade_history = []
        
        # Risk parameters (matching QuantConnect)
        self.max_position_size = 0.40
        self.min_position_size = 0.10
        self.min_trade_value = 50
        self.maker_fee = 0.0016  # 0.16%
        self.taker_fee = 0.0026  # 0.26%
        
        print(f"🚀 Initializing Backtest")
        print(f"   Initial Capital: ${initial_capital:,.2f}")
        print(f"   Symbols: {', '.join(symbols)}")
        print(f"   Fee Model: {self.maker_fee*100:.2f}% maker, {self.taker_fee*100:.2f}% taker")
    
    def fetch_historical_data(self, symbol, days=30):
        """Fetch historical OHLC data from Kraken."""
        print(f"\n📊 Fetching {days} days of data for {symbol}...")
        
        kraken = KrakenAPI()
        pair_map = {
            'BTC': 'XXBTZUSD',
            'ETH': 'XETHZUSD',
            'SOL': 'SOLUSD',
            'ADA': 'ADAUSD'
        }
        
        pair = pair_map.get(symbol)
        if not pair:
            print(f"   ⚠️  Unknown symbol: {symbol}")
            return None
        
        # Fetch daily data
        ohlc_data = kraken.get_ohlc(pair, interval=1440)  # 1440 min = 1 day
        
        if not ohlc_data:
            print(f"   ❌ Failed to fetch data for {symbol}")
            return None
        
        # Convert to DataFrame
        df = pd.DataFrame(ohlc_data, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count'
        ])
        
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        df['close'] = df['close'].astype(float)
        
        # Keep only recent days
        df = df.tail(days).reset_index(drop=True)
        
        print(f"   ✅ Loaded {len(df)} days of data")
        print(f"   Date Range: {df['timestamp'].min().date()} to {df['timestamp'].max().date()}")
        
        return df
    
    def calculate_equal_weight_allocation(self):
        """Calculate equal-weight target allocation."""
        return {symbol: 1.0 / len(self.symbols) for symbol in self.symbols}
    
    def rebalance(self, prices, date):
        """Execute rebalancing based on target allocations."""
        # Get target allocations (equal weight for baseline)
        target_allocations = self.calculate_equal_weight_allocation()
        
        # Calculate current portfolio value
        portfolio_value = self.cash
        for symbol, quantity in self.holdings.items():
            portfolio_value += quantity * prices.get(symbol, 0)
        
        print(f"\n🔄 Rebalancing on {date}")
        print(f"   Portfolio Value: ${portfolio_value:,.2f}")
        
        trades_executed = 0
        
        for symbol, target_weight in target_allocations.items():
            price = prices.get(symbol)
            
            if price is None or price == 0:
                print(f"   ⚠️  No price for {symbol}, skipping")
                continue
            
            # Calculate target value and quantity
            target_value = portfolio_value * target_weight
            current_value = self.holdings[symbol] * price
            target_quantity = target_value / price
            current_quantity = self.holdings[symbol]
            
            # Calculate trade needed
            quantity_diff = target_quantity - current_quantity
            trade_value = abs(quantity_diff * price)
            
            # Skip small trades
            if trade_value < self.min_trade_value:
                continue
            
            # Execute trade
            if quantity_diff > 0:
                # BUY
                cost = quantity_diff * price * (1 + self.taker_fee)
                if cost <= self.cash:
                    self.cash -= cost
                    self.holdings[symbol] += quantity_diff
                    self.trade_history.append({
                        'date': date,
                        'symbol': symbol,
                        'action': 'BUY',
                        'quantity': quantity_diff,
                        'price': price,
                        'value': cost,
                        'fee': quantity_diff * price * self.taker_fee
                    })
                    print(f"   ✅ BUY {quantity_diff:.6f} {symbol} @ ${price:,.2f} = ${cost:,.2f}")
                    trades_executed += 1
            elif quantity_diff < 0:
                # SELL
                quantity_to_sell = abs(quantity_diff)
                proceeds = quantity_to_sell * price * (1 - self.taker_fee)
                self.cash += proceeds
                self.holdings[symbol] -= quantity_to_sell
                self.trade_history.append({
                    'date': date,
                    'symbol': symbol,
                    'action': 'SELL',
                    'quantity': quantity_to_sell,
                    'price': price,
                    'value': proceeds,
                    'fee': quantity_to_sell * price * self.taker_fee
                })
                print(f"   ✅ SELL {quantity_to_sell:.6f} {symbol} @ ${price:,.2f} = ${proceeds:,.2f}")
                trades_executed += 1
        
        if trades_executed == 0:
            print(f"   ℹ️  No trades executed (all within tolerance)")
        
        # Record portfolio state
        final_value = self.cash
        for symbol, quantity in self.holdings.items():
            final_value += quantity * prices.get(symbol, 0)
        
        self.portfolio_history.append({
            'date': date,
            'value': final_value,
            'cash': self.cash,
            'holdings': self.holdings.copy()
        })
    
    def run_backtest(self, days=30, rebalance_frequency=7):
        """Run the backtest over historical data."""
        print(f"\n{'='*60}")
        print(f"🎯 Running Backtest")
        print(f"{'='*60}")
        print(f"Period: Last {days} days")
        print(f"Rebalancing: Every {rebalance_frequency} days")
        
        # Fetch data for all symbols
        data = {}
        for symbol in self.symbols:
            df = self.fetch_historical_data(symbol, days)
            if df is not None:
                data[symbol] = df
        
        if not data:
            print("\n❌ No data available for backtesting")
            return
        
        # Get common dates
        dates = data[self.symbols[0]]['timestamp'].values
        
        print(f"\n📈 Starting Backtest Simulation...")
        
        # Run rebalancing
        rebalance_count = 0
        for i, date in enumerate(dates):
            # Rebalance on schedule
            if i % rebalance_frequency == 0:
                rebalance_count += 1
                
                # Get prices for this date
                prices = {}
                for symbol in self.symbols:
                    if symbol in data:
                        idx = (data[symbol]['timestamp'] == date).idxmax()
                        prices[symbol] = data[symbol].loc[idx, 'close']
                
                self.rebalance(prices, pd.Timestamp(date).date())
        
        print(f"\n{'='*60}")
        print(f"✅ Backtest Complete!")
        print(f"{'='*60}")
        
        self.print_results()
    
    def print_results(self):
        """Print backtest results and statistics."""
        if not self.portfolio_history:
            print("No portfolio history to display")
            return
        
        # Calculate metrics
        initial_value = self.initial_capital
        final_value = self.portfolio_history[-1]['value']
        total_return = ((final_value - initial_value) / initial_value) * 100
        
        # Daily returns
        values = [p['value'] for p in self.portfolio_history]
        returns = np.diff(values) / values[:-1]
        
        # Calculate Sharpe ratio (annualized, assuming 0% risk-free rate)
        if len(returns) > 1:
            sharpe = np.mean(returns) / np.std(returns) * np.sqrt(365/7) if np.std(returns) > 0 else 0
        else:
            sharpe = 0
        
        # Max drawdown
        cummax = np.maximum.accumulate(values)
        drawdowns = (np.array(values) - cummax) / cummax
        max_drawdown = abs(drawdowns.min()) * 100 if len(drawdowns) > 0 else 0
        
        # Win rate
        trades_df = pd.DataFrame(self.trade_history)
        num_trades = len(trades_df)
        
        print(f"\n📊 Performance Summary:")
        print(f"{'='*60}")
        print(f"   Initial Capital:    ${initial_value:,.2f}")
        print(f"   Final Value:        ${final_value:,.2f}")
        print(f"   Total Return:       {total_return:+.2f}%")
        print(f"   Sharpe Ratio:       {sharpe:.2f}")
        print(f"   Max Drawdown:       {max_drawdown:.2f}%")
        print(f"   Total Trades:       {num_trades}")
        print(f"   Rebalances:         {len(self.portfolio_history)}")
        
        # Calculate total fees
        if num_trades > 0:
            total_fees = trades_df['fee'].sum()
            print(f"   Total Fees Paid:    ${total_fees:,.2f} ({(total_fees/initial_value)*100:.2f}%)")
        
        print(f"\n💼 Final Holdings:")
        print(f"{'='*60}")
        final_holdings = self.portfolio_history[-1]['holdings']
        final_cash = self.portfolio_history[-1]['cash']
        
        for symbol, quantity in final_holdings.items():
            if quantity > 0:
                print(f"   {symbol}: {quantity:.6f}")
        print(f"   CASH: ${final_cash:,.2f}")
        
        # Performance vs buy-and-hold BTC
        print(f"\n📈 Performance Analysis:")
        print(f"{'='*60}")
        
        if total_return > 0:
            print(f"   ✅ Strategy: Profitable (+{total_return:.2f}%)")
        else:
            print(f"   ❌ Strategy: Loss ({total_return:.2f}%)")
        
        if sharpe > 1.0:
            print(f"   ✅ Sharpe Ratio: Good risk-adjusted returns ({sharpe:.2f})")
        elif sharpe > 0.5:
            print(f"   ⚠️  Sharpe Ratio: Moderate ({sharpe:.2f})")
        else:
            print(f"   ❌ Sharpe Ratio: Below target ({sharpe:.2f})")
        
        if max_drawdown < 30:
            print(f"   ✅ Drawdown: Well managed ({max_drawdown:.2f}%)")
        elif max_drawdown < 40:
            print(f"   ⚠️  Drawdown: Moderate risk ({max_drawdown:.2f}%)")
        else:
            print(f"   ❌ Drawdown: High risk ({max_drawdown:.2f}%)")
        
        print(f"\n💡 Next Steps:")
        print(f"   1. This is the BASELINE (equal-weight strategy)")
        print(f"   2. Build LSTM model for predictions")
        print(f"   3. Integrate ML predictions to beat this baseline")
        print(f"   4. Goal: Improve Sharpe by 0.3-0.5 points with ML")
        

def main():
    """Run the backtest."""
    print("="*60)
    print("🚀 Crypto ML Strategy - Local Backtest")
    print("="*60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Initialize backtest
    backtest = LocalBacktest(
        initial_capital=5000,
        symbols=['BTC', 'ETH', 'SOL', 'ADA']
    )
    
    # Run backtest on last 90 days with weekly rebalancing
    backtest.run_backtest(days=90, rebalance_frequency=7)
    
    print(f"\n{'='*60}")
    print("🎉 Backtest Complete!")
    print(f"{'='*60}")
    print("\nℹ️  Note: This is a simplified backtest using recent Kraken data.")
    print("   For full 3+ year backtest, use QuantConnect Cloud.")
    print("   This gives you a quick baseline to understand the strategy.")


if __name__ == "__main__":
    main()

