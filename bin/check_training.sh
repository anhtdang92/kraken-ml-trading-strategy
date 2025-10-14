#!/bin/bash

# 📊 Check ML Training Progress

JOB_ID="projects/64620033647/locations/us-central1/customJobs/4173161697067925504"
REGION="us-central1"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  📊 ML Training Progress Checker"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Get job status
echo "🔍 Checking training status..."
echo ""

STATUS=$(gcloud ai custom-jobs describe $JOB_ID --format="value(state)")
CREATE_TIME=$(gcloud ai custom-jobs describe $JOB_ID --format="value(createTime)")

echo "Status: $STATUS"
echo "Started: $CREATE_TIME"
echo ""

case $STATUS in
    "JOB_STATE_PENDING")
        echo "⏳ Job is starting up (takes 2-5 minutes)"
        echo "   Container is being pulled and initialized..."
        echo ""
        echo "✅ What to do: Wait a few minutes, then run this script again"
        ;;
    "JOB_STATE_RUNNING")
        echo "🔄 Training is in progress!"
        echo ""
        echo "📋 Streaming recent logs..."
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        gcloud ai custom-jobs stream-logs $JOB_ID 2>&1 | head -20 || echo "Logs not available yet..."
        ;;
    "JOB_STATE_SUCCEEDED")
        echo "🎉 Training completed successfully!"
        echo ""
        echo "📦 Models have been trained and saved to Cloud Storage"
        echo ""
        echo "✅ Next step: Deploy the models to an endpoint"
        echo "   Run: bash scripts/deployment/deploy_budget_endpoint.sh"
        ;;
    "JOB_STATE_FAILED")
        echo "❌ Training failed"
        echo ""
        echo "📋 Error logs:"
        gcloud ai custom-jobs stream-logs $JOB_ID 2>&1 | tail -30
        ;;
    *)
        echo "❓ Unknown status: $STATUS"
        ;;
esac

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 Track in dashboard: http://localhost:8501 → ☁️ Cloud Progress"
echo "🌐 Web console: https://console.cloud.google.com/vertex-ai/training/custom-jobs"
echo ""
echo "🔄 Run this script again anytime: ./check_training.sh"
echo ""

