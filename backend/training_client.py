"""
FastAPI Training Client
Example script to trigger and monitor training via FastAPI endpoints
"""
import requests
import time
import json
from typing import Dict, Optional


class TrainingClient:
    """Client for interacting with training API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.training_url = f"{base_url}/training"
    
    def start_training(self, name: str = "Personality CNN Model") -> Optional[str]:
        """Start training and return job ID"""
        try:
            response = requests.post(
                f"{self.training_url}/start",
                json={"name": name},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            job_id = data.get("job_id")
            print(f"✅ Training started! Job ID: {job_id}")
            return job_id
        except Exception as e:
            print(f"❌ Error starting training: {e}")
            return None
    
    def get_status(self, job_id: str) -> Optional[Dict]:
        """Get current training status"""
        try:
            response = requests.get(
                f"{self.training_url}/status/{job_id}",
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Error getting status: {e}")
            return None
    
    def monitor_training(self, job_id: str, check_interval: int = 5, max_wait_minutes: int = 120):
        """Monitor training progress until completion"""
        print(f"\n📊 Monitoring Training Job: {job_id}")
        print("="*80)
        
        start_time = time.time()
        max_wait_seconds = max_wait_minutes * 60
        
        while True:
            status = self.get_status(job_id)
            
            if not status:
                print("❌ Failed to get status")
                break
            
            # Display current status
            print(f"\n⏱️  Time Elapsed: {self._format_time(time.time() - start_time)}")
            print(f"Status: {status['status'].upper()}")
            print(f"Progress: {status['progress']:.1f}%")
            print(f"Epoch: {status['current_epoch']}/{status['total_epochs']}")
            
            if status['current_loss'] > 0:
                print(f"Train Loss: {status['current_loss']:.4f}")
            if status['val_loss'] > 0:
                print(f"Val Loss: {status['val_loss']:.4f}")
            if status['accuracy'] > 0:
                print(f"Accuracy: {status['accuracy']:.4f}")
            
            print(f"Message: {status['message']}")
            
            # Check if completed or failed
            if status['status'] in ['completed', 'failed']:
                print("\n" + "="*80)
                if status['status'] == 'completed':
                    print("✅ TRAINING COMPLETED SUCCESSFULLY!")
                else:
                    print(f"❌ TRAINING FAILED: {status.get('error', 'Unknown error')}")
                print("="*80)
                break
            
            # Check timeout
            if time.time() - start_time > max_wait_seconds:
                print("\n⚠️  Training monitor timeout")
                break
            
            # Wait before next check
            time.sleep(check_interval)
    
    def list_jobs(self) -> Optional[Dict]:
        """List all training jobs"""
        try:
            response = requests.get(
                f"{self.training_url}/jobs",
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Error listing jobs: {e}")
            return None
    
    def health_check(self) -> bool:
        """Check if training service is healthy"""
        try:
            response = requests.get(
                f"{self.training_url}/health",
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            print(f"✅ Training service healthy")
            print(f"   Active jobs: {data['active_jobs']}")
            print(f"   Completed jobs: {data['completed_jobs']}")
            return True
        except Exception as e:
            print(f"❌ Training service unavailable: {e}")
            return False
    
    @staticmethod
    def _format_time(seconds: int) -> str:
        """Format seconds to HH:MM:SS"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def main():
    """Example usage"""
    print("\n" + "="*80)
    print("🚀 FASTAPI TRAINING CLIENT")
    print("="*80 + "\n")
    
    client = TrainingClient()
    
    # Check health
    print("1️⃣  Checking service health...")
    if not client.health_check():
        print("\n⚠️  Make sure FastAPI server is running: python -m uvicorn app.main:app --reload")
        return
    
    # Start training
    print("\n2️⃣  Starting training...")
    job_id = client.start_training()
    
    if not job_id:
        print("Failed to start training")
        return
    
    # Monitor training
    print("\n3️⃣  Monitoring training progress...")
    client.monitor_training(job_id, check_interval=5)
    
    # List all jobs
    print("\n4️⃣  All training jobs:")
    jobs = client.list_jobs()
    if jobs:
        print(json.dumps(jobs, indent=2))


if __name__ == "__main__":
    main()
