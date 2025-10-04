# QuantConnect Integration

This directory contains the QuantConnect algorithm for backtesting the Crypto ML Trading Strategy.

## 📋 Algorithm Overview

**File:** `CryptoMLStrategy.py`

### Strategy Details:
- **Assets:** BTC, ETH, SOL, ADA
- **Rebalancing:** Weekly (Sunday 10 PM CDT)
- **Initial Capital:** $5,000
- **Brokerage:** Kraken (0.16% maker, 0.26% taker fees)
- **Backtest Period:** Jan 2022 - Present (3+ years)

### Current Implementation:
- ✅ Equal-weight baseline (25% each asset)
- ✅ Risk constraints (10-40% position sizes)
- ✅ $50 minimum trade size
- ✅ Weekly rebalancing schedule
- ✅ Performance tracking and logging
- ⏳ ML predictions integration (coming next)

## 🚀 Quick Start

### Option 1: Use QuantConnect Cloud (Recommended)

1. **Sign up** at https://www.quantconnect.com/signup (free account)

2. **Create New Algorithm:**
   - Go to: https://www.quantconnect.com/terminal
   - Click "New Algorithm"
   - Name it "Crypto ML Strategy"
   - Language: Python

3. **Copy the code:**
   - Copy contents of `CryptoMLStrategy.py`
   - Paste into QuantConnect editor
   - Click "Save"

4. **Run Backtest:**
   - Click "Backtest" button
   - Wait 2-3 minutes for results
   - View performance charts and statistics

5. **Analyze Results:**
   - Compare vs BTC benchmark
   - Check Sharpe ratio, max drawdown
   - Review trade history

### Option 2: Local Development with Lean CLI

Already installed! To run locally:

```bash
# Activate environment
source venv/bin/activate

# Login to QuantConnect (first time only)
lean login

# Run backtest locally (requires Docker)
lean backtest "quantconnect" --output results/

# View results
lean report results/
```

## 📊 Expected Metrics

### Baseline Strategy (Equal Weight)
- **Goal:** Match or beat BTC buy-and-hold
- **Target Sharpe Ratio:** > 1.0
- **Target Max Drawdown:** < 40%
- **Rebalancing Cost:** ~2-3% annually

### With ML Predictions (Phase 2)
- **Goal:** Outperform baseline by 5-10%
- **Target Sharpe Ratio:** > 1.5
- **Target Max Drawdown:** < 30%
- **Win Rate:** > 55%

## 🔧 Customization

### Adjust Trading Parameters

In `CryptoMLStrategy.py`:

```python
# Line 30: Change start date
self.SetStartDate(2022, 1, 1)

# Line 36: Change initial capital
self.SetCash(10000)  # $10k instead of $5k

# Line 46-47: Adjust risk parameters
self.max_position_size = 0.50  # Allow 50% positions
self.min_position_size = 0.05  # Allow 5% minimum

# Line 49: Change minimum trade size
self.min_trade_value = 100  # $100 minimum
```

### Add More Cryptocurrencies

```python
# Line 40-43: Add more assets
self.symbols['DOT'] = self.AddCrypto("DOTUSD", Resolution.Hour).Symbol
self.symbols['MATIC'] = self.AddCrypto("MATICUSD", Resolution.Hour).Symbol
```

### Change Rebalancing Frequency

```python
# Line 51-55: Change schedule
# Daily at 10 PM
self.Schedule.On(
    self.DateRules.EveryDay(),
    self.TimeRules.At(22, 0),
    self.Rebalance
)

# Or bi-weekly
self.Schedule.On(
    self.DateRules.Every(DayOfWeek.Sunday),
    self.TimeRules.At(22, 0),
    self.Rebalance
).Every(2)
```

## 📈 Integration with ML Model

When ML predictions are ready (Phase 2), update `GetTargetAllocations()`:

```python
def GetTargetAllocations(self):
    """ML-enhanced allocations."""
    # Start with equal weight
    allocations = {symbol: 0.25 for symbol in self.symbols.keys()}
    
    # Load predictions from external source or model
    if self.predictions:
        for symbol_name in self.symbols.keys():
            predicted_return = self.predictions.get(symbol_name, 0)
            
            # Increase allocation for positive predictions
            if predicted_return > 0.05:  # > 5% predicted
                allocations[symbol_name] *= 1.5  # Increase by 50%
            elif predicted_return < -0.05:  # < -5% predicted
                allocations[symbol_name] *= 0.5  # Decrease by 50%
    
    # Apply risk constraints
    # ... (normalize, cap at max/min)
    
    return allocations
```

## 🧪 Testing Strategy

### 1. Baseline Test (Current)
Run the current equal-weight strategy to establish baseline performance.

**Expected:**
- Moderate returns
- Lower volatility than single asset
- Diversification benefits

### 2. ML-Enhanced Test (After Phase 2)
Run with ML predictions integrated.

**Compare:**
- Total return vs baseline
- Sharpe ratio improvement
- Drawdown reduction
- Trade frequency and costs

### 3. Sensitivity Analysis
Test different parameters:
- Rebalancing frequency (daily, weekly, bi-weekly)
- Position size limits (20-40% max)
- Minimum trade sizes ($25, $50, $100)
- Number of assets (4, 6, 8 cryptos)

## 📊 QuantConnect Features

### Available Data:
- ✅ Crypto prices (hourly/daily)
- ✅ Order book depth (premium)
- ✅ Volume data
- ⏳ On-chain metrics (premium)

### Analysis Tools:
- ✅ Performance charts (returns, drawdown)
- ✅ Trade-by-trade analysis
- ✅ Risk metrics (Sharpe, Sortino, Beta)
- ✅ Benchmark comparison
- ✅ Export to CSV/JSON

### Live Trading:
- ⏳ After successful backtesting
- ⏳ Requires Kraken API keys
- ⏳ Paper trading available
- ⏳ Real-time monitoring

## 🔗 Useful Links

- **QuantConnect Docs:** https://www.quantconnect.com/docs/v2
- **Algorithm Lab:** https://www.quantconnect.com/terminal
- **Community Forum:** https://www.quantconnect.com/forum
- **Crypto Trading Guide:** https://www.quantconnect.com/docs/v2/writing-algorithms/datasets/coinapi
- **Kraken Brokerage:** https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/brokerages/supported-models/kraken

## 🎯 Next Steps

1. **Run baseline backtest** on QuantConnect cloud
2. **Analyze results** - note Sharpe ratio, max drawdown
3. **Build ML model** (Phase 2) for predictions
4. **Integrate predictions** into `GetTargetAllocations()`
5. **Re-run backtest** with ML enhancements
6. **Compare performance** vs baseline
7. **Optimize parameters** based on results
8. **Paper trade** before going live

---

**⚠️ Important:** This is for educational purposes. Always paper trade extensively before risking real capital!

