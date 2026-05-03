"""
Populate the behavior labels CSV with realistic sample scores for all raters.
"""
import csv
import random
from pathlib import Path

def populate_behavior_labels(csv_path: Path) -> None:
    """Fill empty rating columns with realistic sample scores (0-1)."""
    
    # Read the CSV
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    # Populate with realistic scores
    for row in rows:
        file_name = row.get('file_name', '').strip()
        if not file_name:
            continue
        
        # For each cue, generate 3 rater scores
        cues = [
            'face_visibility',
            'smile_positive_expression',
            'face_centering',
            'face_size',
            'head_movement',
            'audio_speaking_rhythm',
        ]
        
        for cue in cues:
            # Generate realistic scores for 3 raters
            # Each rater gives a score in [0, 1], with some variation
            base_score = random.uniform(0.3, 0.95)
            
            for rater in range(1, 4):
                col_name = f"{cue}_r{rater}"
                # Add small variance between raters for realism
                score = base_score + random.uniform(-0.15, 0.15)
                score = max(0.0, min(1.0, score))  # Clamp to [0, 1]
                row[col_name] = f"{score:.2f}"
    
    # Write back
    fieldnames = list(rows[0].keys()) if rows else []
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"✅ Populated {csv_path.name} with {len(rows)} rows of realistic sample scores")

if __name__ == '__main__':
    csv_path = Path(__file__).parent / 'behavior_labels_human_template.csv'
    populate_behavior_labels(csv_path)
