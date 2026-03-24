#!/bin/bash

# Local ML Training Launcher
# Train LSTM models on your local GPU (RTX 4090, 3090, etc.) or CPU.
# No Google Cloud required.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ATLAS - Local GPU Training Launcher"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 not found"
    exit 1
fi

# Check TensorFlow
echo "Checking TensorFlow installation..."
GPU_STATUS=$(python3 -c "
import sys
try:
    import tensorflow as tf
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        for gpu in gpus:
            print(f'  GPU found: {gpu.name}')
        # Enable memory growth to avoid grabbing all VRAM
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        print(f'  Total GPUs: {len(gpus)}')
        print('GPU')
    else:
        print('  No GPU detected - will train on CPU (slower)')
        print('CPU')
except ImportError:
    print('  TensorFlow not installed!')
    print('  Run: pip install tensorflow==2.15.0')
    print('MISSING')
    sys.exit(1)
" 2>/dev/null)

DEVICE=$(echo "$GPU_STATUS" | tail -1)
echo ""

if [ "$DEVICE" = "MISSING" ]; then
    echo "Error: TensorFlow not installed. Run: pip install tensorflow==2.15.0"
    exit 1
fi

if [ "$DEVICE" = "GPU" ]; then
    echo "Training will use GPU acceleration"
else
    echo "Training will use CPU (install CUDA toolkit for GPU support)"
fi
echo ""

# Show menu
echo "Choose training option:"
echo ""
echo "1. Quick Training (7 tech stocks)"
echo "   - Stocks: AAPL, MSFT, GOOGL, AMZN, NVDA, META, TSLA"
echo "   - Time: ~2-5 min on GPU, ~15-30 min on CPU"
echo ""
echo "2. Full Training (all 33 stocks)"
echo "   - Stocks: All tracked symbols"
echo "   - Time: ~10-20 min on GPU, ~1-2 hours on CPU"
echo ""
echo "3. Single Stock Training"
echo "   - Train model for one specific symbol"
echo ""
echo "4. Walk-Forward Validation (single stock)"
echo "   - Honest out-of-sample performance evaluation"
echo ""
echo "0. Exit"
echo ""
read -p "Enter choice [0-4]: " choice

case $choice in
    1)
        echo ""
        echo "Starting quick training (7 tech stocks)..."
        echo ""
        cd "$PROJECT_DIR"
        python3 -c "
from ml.prediction_service import PredictionService
ps = PredictionService(provider='local')
symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA']
for i, sym in enumerate(symbols):
    print(f'\n[{i+1}/{len(symbols)}] Training {sym}...')
    result = ps.train_model(sym, days=730, epochs=150)
    if result['status'] == 'success':
        print(f'  Trained: {result[\"training_samples\"]} samples, '
              f'{result[\"epochs_trained\"]} epochs, '
              f'val_loss={result[\"final_val_loss\"]:.6f}')
    else:
        print(f'  Failed: {result.get(\"message\", \"unknown error\")}')
print('\nTraining complete!')
"
        ;;
    2)
        echo ""
        echo "Starting full training (all 33 stocks)..."
        echo ""
        cd "$PROJECT_DIR"
        python3 -c "
from ml.prediction_service import PredictionService
ps = PredictionService(provider='local')
results = ps.train_all_models(days=730, epochs=150)
success = sum(1 for r in results.values() if r['status'] == 'success')
print(f'\nComplete: {success}/{len(results)} models trained successfully')
"
        ;;
    3)
        echo ""
        read -p "Enter stock symbol (e.g. AAPL): " SYMBOL
        SYMBOL=$(echo "$SYMBOL" | tr '[:lower:]' '[:upper:]')
        echo ""
        echo "Training model for $SYMBOL..."
        echo ""
        cd "$PROJECT_DIR"
        python3 -c "
from ml.prediction_service import PredictionService
ps = PredictionService(provider='local')
result = ps.train_model('$SYMBOL', days=730, epochs=150)
if result['status'] == 'success':
    print(f'Training complete!')
    print(f'  Samples: {result[\"training_samples\"]} train, {result[\"validation_samples\"]} val')
    print(f'  Epochs: {result[\"epochs_trained\"]}')
    print(f'  Train loss: {result[\"final_train_loss\"]:.6f}')
    print(f'  Val loss: {result[\"final_val_loss\"]:.6f}')
    m = result.get('metrics', {})
    if m:
        print(f'  Directional accuracy: {m.get(\"directional_accuracy\", 0):.1%}')
        print(f'  MAE: {m.get(\"mae\", 0):.4f}')
else:
    print(f'Failed: {result.get(\"message\", \"unknown error\")}')
"
        ;;
    4)
        echo ""
        read -p "Enter stock symbol (e.g. AAPL): " SYMBOL
        SYMBOL=$(echo "$SYMBOL" | tr '[:lower:]' '[:upper:]')
        echo ""
        echo "Running walk-forward validation for $SYMBOL (5 folds)..."
        echo "This tests if the model has a real edge out-of-sample."
        echo ""
        cd "$PROJECT_DIR"
        python3 -c "
from ml.prediction_service import PredictionService
ps = PredictionService(provider='local')
result = ps.walk_forward_validate('$SYMBOL', n_splits=5, days=730, epochs=100)
if result['status'] == 'success':
    agg = result['aggregate_metrics']
    print(f'\nWalk-Forward Results for $SYMBOL ({result[\"n_folds\"]} folds):')
    print(f'  Avg Directional Accuracy: {agg[\"avg_directional_accuracy\"]:.1%} (need >53%)')
    print(f'  Std Directional Accuracy: {agg[\"std_directional_accuracy\"]:.1%}')
    print(f'  Avg MAE: {agg[\"avg_mae\"]:.4f}')
    print(f'  Avg RMSE: {agg[\"avg_rmse\"]:.4f}')
    print(f'  Avg Info Coefficient: {agg[\"avg_ic\"]:.4f}')
    if agg['avg_directional_accuracy'] > 0.53:
        print('\n  PASS - Model shows edge over random.')
    else:
        print('\n  FAIL - Model does not beat random. Do not trade on this.')
else:
    print(f'Failed: {result.get(\"message\", \"unknown error\")}')
"
        ;;
    0)
        echo "Goodbye!"
        exit 0
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Done!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Next steps:"
echo "  1. Run the dashboard: streamlit run app.py"
echo "  2. Check ML Predictions tab for real predictions"
echo "  3. Run walk-forward validation before trading"
echo ""
