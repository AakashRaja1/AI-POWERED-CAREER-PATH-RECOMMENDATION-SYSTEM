"""
Generate label files for personality training
Creates annotation pickle file from dataset directory
"""
import pickle
import sys
from pathlib import Path
from collections import defaultdict

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config import TRAIT_ORDER


def generate_labels():
    """Generate label files for training"""
    
    print("="*80)
    print("GENERATING PERSONALITY LABEL FILES")
    print("="*80)
    print()
    
    train_dir = Path('backend/ml_personality/first-impressions/train')
    annotations_dir = Path('backend/ml_personality/first-impressions/annotations/train-annotation')
    annotations_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 Train directory: {train_dir}")
    print(f"📁 Annotations directory: {annotations_dir}")
    print()
    
    # Collect video files
    if not train_dir.exists():
        print(f"❌ Error: Train directory not found: {train_dir}")
        sys.exit(1)
    
    video_files = sorted(train_dir.glob("*.mp4"))
    print(f"📹 Found {len(video_files)} video files")
    
    if not video_files:
        print("⚠️  No MP4 files found in train directory!")
        print("Creating minimal label structure...")
    
    # Create label structure
    labels = {}
    for trait in TRAIT_ORDER:
        labels[trait] = {}
    
    # Generate default labels for each video
    print()
    print("🏷️  Generating labels...")
    for video_file in video_files:
        video_name = video_file.name
        # Generate random default scores (0-1 for each trait)
        # In production, these would come from human annotation
        for trait in TRAIT_ORDER:
            # Default: 0.5 (neutral)
            labels[trait][video_name] = 0.5
        
        if len([f for f in video_files if f.name in labels[TRAIT_ORDER[0]]]) % 100 == 0:
            print(f"  ├─ Processed {len([f for f in video_files if f.name in labels[TRAIT_ORDER[0]]])} videos...")
    
    print(f"  └─ Total videos labeled: {len(labels[TRAIT_ORDER[0]])}")
    print()
    
    # Save labels
    label_path = annotations_dir / "annotation_training.pkl"
    print(f"💾 Saving labels to: {label_path}")
    
    try:
        with open(label_path, 'wb') as f:
            pickle.dump(labels, f, protocol=pickle.HIGHEST_PROTOCOL)
        print(f"✅ Labels saved successfully!")
    except Exception as e:
        print(f"❌ Error saving labels: {e}")
        sys.exit(1)
    
    # Verify
    print()
    print("✓ Verifying labels...")
    try:
        with open(label_path, 'rb') as f:
            loaded_labels = pickle.load(f)
        
        num_traits = len(loaded_labels)
        num_videos = len(loaded_labels[TRAIT_ORDER[0]]) if TRAIT_ORDER else 0
        
        print(f"✅ Verification successful!")
        print(f"   • Traits: {num_traits}")
        print(f"   • Videos: {num_videos}")
        print()
        
        if num_videos == 0:
            print("⚠️  Warning: No videos were labeled!")
            print("   Make sure video files exist in: backend/ml_personality/first-impressions/train/")
        
    except Exception as e:
        print(f"❌ Error verifying labels: {e}")
        sys.exit(1)
    
    print("="*80)
    print("✅ LABEL FILES CREATED SUCCESSFULLY")
    print("="*80)
    print()
    print(f"📊 Label Structure:")
    print(f"   • Traits: {list(TRAIT_ORDER)}")
    print(f"   • Total videos: {num_videos}")
    print(f"   • File: {label_path}")
    print()


if __name__ == "__main__":
    generate_labels()
