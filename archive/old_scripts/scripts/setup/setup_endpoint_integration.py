#!/usr/bin/env python3
"""
Setup script to integrate Vertex AI endpoint with trading system
"""

import os
import sys

def setup_environment():
    """Set up environment variables for Vertex AI integration"""
    
    print("🔧 Setting up Vertex AI endpoint integration...")
    
    # Set environment variables for current session
    os.environ['GOOGLE_CLOUD_PROJECT'] = 'crypto-ml-trading-487'
    os.environ['GCP_REGION'] = 'us-central1'
    os.environ['VERTEX_ENDPOINT_ID'] = '1074806701011501056'
    os.environ['PAPER_TRADING'] = 'true'
    
    print("✅ Environment variables set:")
    print(f"   GOOGLE_CLOUD_PROJECT: {os.environ['GOOGLE_CLOUD_PROJECT']}")
    print(f"   GCP_REGION: {os.environ['GCP_REGION']}")
    print(f"   VERTEX_ENDPOINT_ID: {os.environ['VERTEX_ENDPOINT_ID']}")
    print(f"   PAPER_TRADING: {os.environ['PAPER_TRADING']}")

def test_integration():
    """Test the endpoint integration"""
    
    print("\n🧪 Testing endpoint integration...")
    
    try:
        from ml.prediction_service import PredictionService
        
        # Initialize prediction service with Vertex AI
        service = PredictionService(provider="vertex")
        
        # Test prediction
        print("   Testing prediction for BTC...")
        prediction = service.get_prediction('BTC', days_ahead=7)
        
        print(f"   ✅ Prediction result:")
        print(f"      Symbol: {prediction['symbol']}")
        print(f"      Current Price: ${prediction['current_price']:,.2f}")
        print(f"      Predicted Price: ${prediction['predicted_price']:,.2f}")
        print(f"      Predicted Return: {prediction['predicted_return']*100:+.2f}%")
        print(f"      Confidence: {prediction['confidence']*100:.1f}%")
        print(f"      Status: {prediction['status']}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Integration test failed: {e}")
        return False

def test_rebalancing():
    """Test portfolio rebalancing with Vertex AI"""
    
    print("\n🔄 Testing portfolio rebalancing...")
    
    try:
        from ml.portfolio_rebalancer import PortfolioRebalancer
        
        # Initialize rebalancer
        rebalancer = PortfolioRebalancer(paper_trading=True)
        
        # Get rebalancing summary
        print("   Getting rebalancing recommendations...")
        summary = rebalancer.get_rebalancing_summary()
        
        print(f"   ✅ Rebalancing summary:")
        print(f"      Total trades: {summary['metrics']['total_trades']}")
        print(f"      Total fees: ${summary['metrics']['total_fees']:.2f}")
        print(f"      Buy orders: {summary['metrics']['buy_orders']}")
        print(f"      Sell orders: {summary['metrics']['sell_orders']}")
        print(f"      Max drift: {summary['metrics']['max_drift']*100:.2f}%")
        
        # Show recommendations
        if summary['recommendations']:
            print("   📋 Recommendations:")
            for rec in summary['recommendations']:
                print(f"      {rec}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Rebalancing test failed: {e}")
        return False

def main():
    """Main setup function"""
    
    print("="*60)
    print("🚀 Vertex AI Endpoint Integration Setup")
    print("="*60)
    
    # Setup environment
    setup_environment()
    
    # Test integration
    prediction_success = test_integration()
    rebalancing_success = test_rebalancing()
    
    # Summary
    print("\n" + "="*60)
    print("📊 Integration Summary")
    print("="*60)
    
    if prediction_success:
        print("✅ Prediction Service: Working")
    else:
        print("❌ Prediction Service: Failed")
    
    if rebalancing_success:
        print("✅ Portfolio Rebalancer: Working")
    else:
        print("❌ Portfolio Rebalancer: Failed")
    
    if prediction_success and rebalancing_success:
        print("\n🎉 Endpoint integration successful!")
        print("\n📝 Next steps:")
        print("   1. Run your Streamlit dashboard: streamlit run app.py")
        print("   2. Navigate to the 'ML Predictions' page")
        print("   3. Navigate to the 'Rebalancing' page")
        print("   4. Test the integrated system")
    else:
        print("\n⚠️ Some components failed. Check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
