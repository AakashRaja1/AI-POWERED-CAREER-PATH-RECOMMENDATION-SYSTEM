# FastAPI Training - Quick Reference

## 🚀 Start FastAPI Server

```powershell
cd backend
(& "venv\Scripts\Activate.ps1")
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Server will be available at: http://localhost:8000

---

## 📊 Start Training

### Option 1: Python Client (EASIEST)
```powershell
cd backend
python training_client.py
```
✅ Shows live progress with epochs and metrics

### Option 2: Browser/Postman
1. Open: http://localhost:8000/docs (Swagger UI)
2. Find `/training/start` endpoint
3. Click "Try it out" → Execute
4. Note the `job_id`
5. Use `job_id` in `/training/status/{job_id}`

### Option 3: curl
```bash
# Start training
curl -X POST http://localhost:8000/training/start

# Get job_id from response, then:
curl http://localhost:8000/training/status/{job_id}
```

---

## 📈 Monitor Progress

**Check status:**
```powershell
$job_id = "abc123"
Invoke-RestMethod "http://localhost:8000/training/status/$job_id" | ConvertTo-Json
```

**Watch live (every 5 seconds):**
```powershell
while ($true) {
  $status = Invoke-RestMethod "http://localhost:8000/training/status/YOUR_JOB_ID"
  Write-Host "Progress: $($status.progress)% | Epoch: $($status.current_epoch)/$($status.total_epochs)"
  Start-Sleep -Seconds 5
}
```

---

## 📋 All Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/training/start` | POST | Start new training |
| `/training/status/{job_id}` | GET | Get current status |
| `/training/jobs` | GET | List all jobs |
| `/training/health` | GET | Check service health |

---

## 📊 Response Example

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
  "message": "Training CNN model for 20 epochs..."
}
```

---

## ⏱️ Status Values

- **pending** → Waiting to start
- **running** → Currently training
- **completed** → ✅ Finished successfully
- **failed** → ❌ Training error

---

## 💾 Output Location

```
backend/ml_personality_pipeline/artifacts/
├── personality_model.pth           # Best model
├── personality_model.metadata.json # Metadata
└── training_report.json            # All metrics
```

---

## 🎯 Training Details

- **Model**: CNN (ResNet18)
- **Device**: CPU
- **Epochs**: 20
- **Time**: ~50-100 minutes
- **Batch Size**: 8
- **Learning Rate**: 1e-4

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Connection refused | Is FastAPI running? Check port 8000 |
| Job not found | Wrong job_id? Job older than server restart |
| Training failed | Check error in status response |
| Slow training | Normal for CPU. ~50-100 min for 20 epochs |

---

## 📚 Full Documentation

See: `FASTAPI_TRAINING_GUIDE.md`

---

**Quick Start:**
```powershell
# Terminal 1: Start FastAPI
cd backend && python -m uvicorn app.main:app --reload

# Terminal 2: Run client and monitor training
cd backend && python training_client.py
```
