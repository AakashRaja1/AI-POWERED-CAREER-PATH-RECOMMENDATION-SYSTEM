Usage: End-to-end processing + training pipeline (CPU)

Prerequisites
- Create and activate a Python virtual environment
- Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Quick steps
1. Extract frames and build labels.csv (example):

```bash
python process_videos.py --input-dir ../ml_personality/first-impressions/train --annotations ../ml_personality/annotations/your_labels.csv --out-root processed_dataset --fps 1.0
```

2. Train CNN classifier on extracted frames:

```bash
python train.py --mode cnn --dataset-root processed_dataset --labels-csv processed_dataset/labels.csv --outputs-root processed_dataset/outputs --epochs 10 --batch-size 4
```

3. Evaluate:

```bash
python evaluate.py --mode cnn --model-path processed_dataset/outputs/models/model.pth --dataset-root processed_dataset --labels-csv processed_dataset/labels.csv --split val
```

4. Inference on a single image:

```bash
python inference.py processed_dataset/frames/some_image.jpg --mode cnn --model-path processed_dataset/outputs/models/model.pth
```

Notes
- Keep `--batch-size` <= 8 for CPU training.
- Use `--max-frames-per-video` to limit frames during extraction for quicker tests.
- The runner script `run_full_pipeline.py` (if present) will execute extraction then training sequentially.
- Outputs are saved inside the provided `--out-root` under `models`, `logs`, and `plots`.