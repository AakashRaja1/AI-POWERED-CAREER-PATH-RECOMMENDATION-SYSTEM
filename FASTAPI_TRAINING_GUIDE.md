# FastAPI Training Integration

Your CPU training is now integrated into the existing FastAPI project! Start training directly from the API.

---

## Quick Start

### 1. Start the FastAPI Server

```powershell
cd backend
(& "venv\Scripts\Activate.ps1")
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Start Training via API

**Option A: Using Python Client (Easiest)**
```powershell
cd backend
python training_client.py
```
Shows live progress with epoch updates ✅

**Option B: Using curl**
```bash
curl -X POST http://localhost:8000/training/start \
  -H "Content-Type: application/json" \
  -d '{"name": "Personality CNN Model"}'
```
Returns: `{"job_id": "abc123...", "status": "pending", "message": "Training started!"}`

**Option C: Using requests in Python**
```python
import requests

# Start training
response = requests.post("http://localhost:8000/training/start")
job_id = response.json()["job_id"]
print(f"Job ID: {job_id}")

# Get status
status = requests.get(f"http://localhost:8000/training/status/{job_id}")
print(status.json())
```

---

## API Endpoints

### POST `/training/start`
Start a new training job

**Request:**
```json
{
  "name": "Personality CNN Model"
}
```

**Response:**
```json
{
  "job_id": "abc123-def456",
  "status": "pending",
  "message": "Training started! Job ID: abc123-def456"
}
```

---

### GET `/training/status/{job_id}`
Get current training status and progress

**Parameters:**
- `job_id`: Job ID from `/training/start` response

**Response:**
```json
{
  "job_id": "abc123-def456",
  "status": "running",
  "progress": 45.0,
  "current_epoch": 9,
  "total_epochs": 20,
  "current_loss": 0.0234,
  "val_loss": 0.0312,
  "accuracy": 0.9127,
  "message": "Training CNN model for 20 epochs...",
  "started_at": "2026-04-28T10:30:00.123456",
  "completed_at": null,
  "error": null
}
```

**Status values:**
- `pending` - Job queued, waiting to start
- `running` - Currently training
- `completed` - Training finished successfully
- `failed` - Training failed with error

---

### GET `/training/jobs`
List all training jobs (completed and in progress)

**Response:**
```json
{
  "jobs": [
    {
      "job_id": "abc123",
      "status": "completed",
      "progress": 100.0,
      "current_epoch": 20,
      "total_epochs": 20,
      "message": "Training completed! Model saved...",
      "started_at": "2026-04-28T10:30:00",
      "completed_at": "2026-04-28T11:45:00"
    }
  ],
  "total": 1
}
```

---

### GET `/training/health`
Check if training service is healthy

**Response:**
```json
{
  "status": "healthy",
  "active_jobs": 1,
  "completed_jobs": 3
}
```

---

## Training Configuration

The training runs with these optimized settings:

```
📊 Training Configuration (CPU-Optimized):
┌──────────────────────────────┬─────────┐
│ Model Architecture           │ CNN     │
│ Backbone                     │ ResNet18│
│ Device                       │ CPU     │
│ Total Epochs                 │ 20      │
│ Batch Size                   │ 8       │
│ Learning Rate                │ 1e-4    │
│ Dataset Split (Train/Val)    │ 85/15   │
│ Early Stopping Patience      │ 8 epochs│
│ Estimated Training Time      │ 50-100m │
└──────────────────────────────┴─────────┘
```

---

## Usage Examples

### Example 1: Python Script with Progress Monitoring

```python
from backend.training_client import TrainingClient

# Initialize client
client = TrainingClient(base_url="http://localhost:8000")

# Start training
job_id = client.start_training("My Personality Model")

# Monitor live progress
client.monitor_training(job_id, check_interval=5)

# Get final status
final_status = client.get_status(job_id)
print(f"Final accuracy: {final_status['accuracy']}")
```

### Example 2: Check Training Status

```python
import requests

job_id = "abc123-def456"
response = requests.get(f"http://localhost:8000/training/status/{job_id}")
status = response.json()

if status['status'] == 'running':
    print(f"Training {status['progress']:.1f}% complete")
    print(f"Epoch {status['current_epoch']}/{status['total_epochs']}")
    print(f"Val Loss: {status['val_loss']:.4f}")
elif status['status'] == 'completed':
    print(f"✅ Training complete! Accuracy: {status['accuracy']:.4f}")
elif status['status'] == 'failed':
    print(f"❌ Training failed: {status['error']}")
```

### Example 3: List All Jobs

```python
import requests
import json

response = requests.get("http://localhost:8000/training/jobs")
jobs = response.json()

print(f"Total training jobs: {jobs['total']}")
for job in jobs['jobs']:
    print(f"\nJob: {job['job_id']}")
    print(f"  Status: {job['status']}")
    print(f"  Progress: {job['progress']:.1f}%")
    print(f"  Started: {job['started_at']}")
```

---

## Output Files

After training completes, check:

```
backend/ml_personality_pipeline/artifacts/
├── personality_model.pth              # Best trained model
├── personality_model.metadata.json    # Model metadata
└── training_report.json               # Complete training metrics
```

---

## Integration Points

The training is integrated into your FastAPI project:

### File Structure
```
backend/
├── app/
│   ├── api/
│   │   └── routers/
│   │       ├── training.py            ✨ NEW: Training endpoints
│   │       └── ...
│   ├── services/
│   │   ├── training_service.py        ✨ NEW: Training service
│   │   └── ...
│   └── main.py                         ✏️ MODIFIED: Added training router
├── ml_personality_pipeline/
│   ├── train_cpu.py                   ✨ NEW: CPU training script
│   ├── train.py                       ✏️ MODIFIED: Added live progress
│   └── generate_labels.py             ✨ NEW: Label generation
├── training_client.py                  ✨ NEW: API client
└── ...
```

### How It Works
1. **Frontend/External Request** → Calls `POST /training/start`
2. **FastAPI Endpoint** → Creates job, starts background thread
3. **Background Training** → Runs `ml_personality_pipeline.train()` with monitoring
4. **Job Status Updates** → Real-time progress via `/training/status/{job_id}`
5. **Model Saved** → Best model automatically saved to artifacts/

---

## Monitoring Training

### Real-Time Monitoring (Python Client)
```bash
cd backend
python training_client.py
```

### Manual Status Checks (Browser/Postman)
- Start: `POST http://localhost:8000/training/start`
- Check Progress: `GET http://localhost:8000/training/status/{job_id}`
- List Jobs: `GET http://localhost:8000/training/jobs`
- Health: `GET http://localhost:8000/training/health`

### curl Command
```bash
# Get status every 10 seconds
watch -n 10 'curl -s http://localhost:8000/training/status/YOUR_JOB_ID | jq .'
```

---

## Troubleshooting

### "Job not found"
- Job ID is incorrect
- Job was created but server restarted (jobs not persisted)

### "Connection refused"
- FastAPI server not running
- Wrong host/port - check `http://localhost:8000`

### "Training failed"
- Check error message in `/training/status/{job_id}`
- Check FastAPI server logs for details
- Ensure dataset and annotation files exist

### Very Slow Training
- CPU training inherently slower than GPU (50-100 min vs 10-15 min)
- Reduce batch_size in `training_service.py` if out of memory

---

## Next Steps

1. ✅ API is integrated
2. 🚀 Start FastAPI server
3. 📊 Call `/training/start` to begin training
4. 🎯 Monitor with `/training/status/{job_id}`
5. 💾 Model auto-saved to artifacts/

**Ready to train?**
```powershell
cd backend
python training_client.py
```

---

**Questions?** Check API documentation at `http://localhost:8000/docs` (Swagger UI)
