# Extra Traits Supervised Training

You can now train the personality model with additional supervised traits (for example confidence/professionalism) by supplying a JSON file with per-media labels.

## Label format

Use a JSON object where each key is a media filename and each value is a trait map with values in [0, 1].

See [extra_traits_labels_example.json](extra_traits_labels_example.json) for an example.

## Train command

Run from backend/ml_personality_pipeline:

```powershell
python train.py --run-profile high --extra-labels-json extra_traits_labels_example.json --extra-traits confidence_score,professionalism_score,communication_score,leadership_potential
```

This uses the heavy/high end-to-end profile.

Use these presets when needed:

- `--run-profile light` for quick sanity checks
- `--run-profile moderate` for balanced iteration
- `--run-profile high` for strongest training quality

## Notes

- Filenames in JSON must match files in your training split directory.
- Samples missing one or more requested extra traits are skipped.
- Inference responses include:
  - `traits`: Big Five predictions
  - `direct_traits`: directly predicted extra supervised traits (if model was trained with them)
  - `derived_scores`: heuristic composites from Big Five

## Evaluate quality

Run from backend/ml_personality_pipeline:

```powershell
python evaluate.py --split train --subset-ratio 1.0 --extra-labels-json extra_traits_labels_example.json --extra-traits confidence_score,professionalism_score,communication_score,leadership_potential
```

This writes a JSON report (for example `artifacts/evaluation_report_train.json`) with:

- Overall MAE and RMSE
- Per-trait MAE, RMSE, and Pearson correlation
