# CPU Training with Live Progress

## Quick Start

### Option 1: Windows Batch Script (Easiest)
```bash
START_CPU_TRAINING.bat
```
Just double-click this file and training will start with LIVE PROGRESS display.

### Option 2: Python Launcher
```powershell
python start_cpu_training.py
```

### Option 3: Direct Training Script
```powershell
(& "venv\Scripts\Activate.ps1")
python backend/ml_personality_pipeline/train_cpu.py
```

---

## What You'll See

### Live Progress Display:
```
Epochs: 45%|████▌     | 9/20 [15:32<18:45, 102.74s/epoch]
  ├─ Training: 100%|██████████| 95/95 [03:45<00:00, 2.37s/batch]
  ├─ Validating: 100%|██████████| 17/17 [00:42<00:00, 2.47s/batch]
  ├─ Train Loss: 0.0234 | Val Loss: 0.0312 | Train Acc: 0.9456 | Val Acc: 0.9127
  ✓ Best model saved! (Loss: 0.0312)
```

### Real-Time Metrics:
- **Per-batch progress**: Loss and MAE for each batch as it trains
- **Per-epoch summary**: Training/validation loss, accuracy, and best model updates
- **Overall time**: Elapsed time and estimated time remaining

---

## Training Details

### Configuration
| Parameter | Value | Reason |
|-----------|-------|--------|
| **Model** | CNN (ResNet18) | Deep learning for personality traits |
| **Device** | CPU (Multi-threaded) | Optimized for your system |
| **Epochs** | 20 | Extended training for best accuracy |
| **Batch Size** | 8 | CPU-optimized memory usage |
| **Learning Rate** | 1e-4 | Fine-tuned convergence |
| **Dataset** | 100% | All available training data |
| **Validation Split** | 15% | Balanced train/validation |

### Expected Performance
- **Training Time**: 50-100 minutes (depending on CPU)
- **Batches per Epoch**: ~95 training, ~17 validation
- **Best Model**: Saved automatically when validation loss improves
- **Early Stopping**: Stops if no improvement for 8 epochs

---

## Output Files

After training completes, check:

```
backend/ml_personality_pipeline/artifacts/
├── personality_model.pth          # Best trained model (checkpoint)
├── personality_model.metadata.json # Model metadata & configuration
└── training_report.json           # Complete training metrics
```

### Training Report includes:
```json
{
  "summary": {
    "epochs_requested": 20,
    "epochs_completed": 20,
    "best_val_loss": 0.0312,
    "best_model_path": "...",
    "validation_split_ratio": 0.15
  },
  "epochs": [
    {
      "epoch": 1,
      "train_loss": 0.1234,
      "val_loss": 0.1456,
      "train_mae": 0.0789,
      "val_mae": 0.0912,
      "train_accuracy": 0.8234,
      "val_accuracy": 0.8012
    },
    ...
  ]
}
```

---

## Monitoring Training

### During Training:
1. Watch the progress bars update in real-time
2. Check metrics at each epoch
3. See when the model is saved (best validation loss)

### Keyboard Controls:
- **Ctrl+C**: Gracefully interrupt training (will ask for confirmation)
- Training state is saved, so you can restart later

### CPU Usage:
The script uses all available CPU threads for faster training.
- Monitor with Task Manager → Performance tab
- CPU usage should be high (80-100%) during batch processing

---

## Troubleshooting

### "No labeled samples found"
- Ensure dataset is in: `backend/ml_personality/first-impressions/train/`
- Check annotation file: `backend/ml_personality/first-impressions/annotations/train-annotation/annotation_training.pkl`

### "CUDA not available" (CPU script)
- This is expected! CPU scripts automatically use CPU
- No CUDA setup needed for CPU training

### Out of Memory
- Reduce batch size in `train_cpu.py` from 8 to 4
- Reduce dataset with `subset_ratio=0.5` for 50% of data

### Very Slow Training
- CPU training is inherently slower than GPU (50-100 min vs 10-15 min)
- Consider using GPU if you need faster training (see `START_GPU_TRAINING.bat`)

---

## Next Steps

After training completes:
1. Review `training_report.json` for metrics
2. Use the model in `inference.py` for personality prediction
3. Evaluate on test set if available
4. Deploy model to production

---

**Questions?** Check the training report and logs for detailed metrics! 🚀
