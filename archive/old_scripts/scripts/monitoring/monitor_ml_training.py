#!/usr/bin/env python3
"""
Monitor ML Training Job
This script monitors the current ML training job and provides updates
"""

import subprocess
import json
import time
from datetime import datetime

def get_job_status(job_id):
    """Get the status of a training job"""
    try:
        result = subprocess.run([
            'gcloud', 'ai', 'custom-jobs', 'describe',
            job_id,
            '--format=json'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            return json.loads(result.stdout)
        return None
    except Exception:
        return None

def monitor_training_job():
    """Monitor the current training job"""
    job_id = "projects/64620033647/locations/us-central1/customJobs/3991464376920965120"
    
    print("🚀 ML Training Job Monitor")
    print("=" * 50)
    print(f"Job ID: {job_id}")
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("")
    
    status_history = []
    
    while True:
        # Get current status
        job_info = get_job_status(job_id)
        
        if job_info:
            state = job_info.get('state', 'UNKNOWN')
            display_name = job_info.get('displayName', 'Unknown')
            create_time = job_info.get('createTime', '')
            
            # Track status changes
            if state not in status_history:
                status_history.append(state)
                timestamp = datetime.now().strftime('%H:%M:%S')
                print(f"[{timestamp}] Status changed to: {state}")
                
                if state == 'JOB_STATE_RUNNING':
                    print("   🎯 Training has started!")
                elif state == 'JOB_STATE_SUCCEEDED':
                    print("   ✅ Training completed successfully!")
                    print("   📦 Model should be saved to Cloud Storage")
                    break
                elif state == 'JOB_STATE_FAILED':
                    print("   ❌ Training failed")
                    print("   📋 Check logs for details")
                    break
            
            # Show current status
            print(f"Current Status: {state} ({display_name})")
            
            # If running, show estimated time
            if state == 'JOB_STATE_RUNNING':
                elapsed = datetime.now() - datetime.fromisoformat(create_time.replace('Z', '+00:00'))
                print(f"Elapsed Time: {elapsed}")
                print("Expected Duration: ~5-10 minutes")
        
        else:
            print("❌ Unable to get job status")
        
        print("-" * 30)
        
        # Check if job is finished
        if state in ['JOB_STATE_SUCCEEDED', 'JOB_STATE_FAILED', 'JOB_STATE_CANCELLED']:
            break
        
        # Wait before next check
        time.sleep(30)
    
    # Final summary
    print("\n" + "=" * 50)
    print("📊 Training Job Summary")
    print("=" * 50)
    
    if job_info:
        final_state = job_info.get('state', 'UNKNOWN')
        print(f"Final Status: {final_state}")
        print(f"Job Name: {job_info.get('displayName', 'Unknown')}")
        
        if final_state == 'JOB_STATE_SUCCEEDED':
            print("\n🎉 Training completed successfully!")
            print("📋 Next steps:")
            print("   1. Check Cloud Storage for the trained model")
            print("   2. Deploy the model to your endpoint")
            print("   3. Test real ML predictions")
        elif final_state == 'JOB_STATE_FAILED':
            print("\n❌ Training failed")
            print("📋 Troubleshooting:")
            print("   1. Check the logs for error details")
            print("   2. Your enhanced mock system is still working")
            print("   3. You can retry training with different parameters")
        else:
            print(f"\n⚠️ Training ended with status: {final_state}")

def main():
    """Main monitoring function"""
    try:
        monitor_training_job()
    except KeyboardInterrupt:
        print("\n\n⏹️ Monitoring stopped by user")
    except Exception as e:
        print(f"\n❌ Error monitoring training job: {e}")

if __name__ == "__main__":
    main()
