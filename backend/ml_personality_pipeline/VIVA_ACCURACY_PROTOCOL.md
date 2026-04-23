# Viva Accuracy Protocol (Defensible and Reproducible)

This protocol helps you answer viva questions with evidence.

## Important truth first

No ML model can be guaranteed "perfect" on unseen real-world data. The correct scientific goal is:

- high quality labels
- reproducible training
- transparent metrics on held-out data
- clear limits and uncertainty

## 1) Create human labeling sheet

Run in `backend/ml_personality_pipeline`:

```powershell
python create_labeling_sheet.py --media-dir ../ml_personality/first-impressions/train --output labels_human_template.csv --num-raters 3
```

Share `labels_human_template.csv` with at least 3 independent raters.

## 2) Aggregate labels + quality report

After raters fill values in [0,1], run:

```powershell
python aggregate_human_labels.py --input-csv labels_human_template.csv --output-json extra_traits_labels_human.json --quality-report artifacts/label_quality_report.json --min-raters 2
```

Artifacts produced:

- `extra_traits_labels_human.json` (used for training)
- `artifacts/label_quality_report.json` (rater consistency evidence)

## 3) Train model with supervised extra traits

```powershell
python train.py --run-profile high --extra-labels-json extra_traits_labels_human.json --extra-traits confidence_score,professionalism_score,communication_score,leadership_potential
```

For an even heavier run, override profile values explicitly:

```powershell
python train.py --run-profile high --epochs 25 --subset-ratio 1.0 --patience 8 --learning-rate 0.0003 --extra-labels-json extra_traits_labels_human.json --extra-traits confidence_score,professionalism_score,communication_score,leadership_potential
```

## 4) Evaluate objectively (per-trait)

```powershell
python evaluate.py --split train --subset-ratio 1.0 --extra-labels-json extra_traits_labels_human.json --extra-traits confidence_score,professionalism_score,communication_score,leadership_potential
```

For stronger evidence, also evaluate on `--split val` and `--split test` when labels are available for those splits.

## 5) Export feature vectors (for technical explanation)

```powershell
python export_feature_vectors.py --media-dir ../ml_personality/first-impressions/train --max-files 500 --frames-per-video 6 --output artifacts/feature_vectors.pt --meta-output artifacts/feature_vectors_meta.json
```

Artifacts produced:

- `artifacts/feature_vectors.pt` (filenames + embedding tensor)
- `artifacts/feature_vectors_meta.json`

## What to say in viva

1. Labels are human-annotated by multiple raters and aggregated.
2. Label quality is measured and reported (`label_quality_report.json`).
3. Model is evaluated with MAE/RMSE/Pearson per trait (`evaluation_report_*.json`).
4. Feature extraction is explainable via pretrained ResNet embeddings (`feature_vectors.pt`).
5. Claims are evidence-based, not "perfect accuracy" claims.
