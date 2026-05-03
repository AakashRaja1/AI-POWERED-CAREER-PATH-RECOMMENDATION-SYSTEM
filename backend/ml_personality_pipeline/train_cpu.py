"""
CPU-focused training script for machines without GPU access. It keeps the same training goal while using settings that are practical on local hardware.

Presentation note: explain this file as one focused responsibility in the larger system, then mention the main inputs it receives and the output it returns or prepares.
"""

import torch
import sys
from pathlib import Path
from tqdm import tqdm
import time

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config import PersonalityConfig
from train import train


def main():
    print("\n" + "="*80)
    print(" " * 20 + "🖥️  CPU PERSONALITY CNN TRAINING 🖥️")
    print("="*80)
    print()
    
    # Check device
    device = torch.device('cpu')
    cpu_count = torch.get_num_threads()
    print(f"📊 System Information:")
    print(f"   Device: {device}")
    print(f"   CPU Threads: {cpu_count}")
    print()
    
    # CPU-optimized training profile
    config = PersonalityConfig(
        train_dir=Path('backend/ml_personality/first-impressions/train'),
        train_annotation=Path('backend/ml_personality/first-impressions/annotations/train-annotation/annotation_training.pkl'),
        subset_ratio=1.0,  # Use all data
        epochs=20,  # Standard training
        batch_size=8,  # Smaller batch for CPU memory efficiency
        learning_rate=1e-4,  # Fine-tuned learning rate
        patience=8,  # Early stopping patience
        validation_split_ratio=0.15,  # 15% validation data
    )
    
    print("📋 Training Configuration:")
    print(f"   Model Architecture: CNN (ResNet18)")
    print(f"   Device: CPU (Multi-threaded)")
    print(f"   Total Epochs: {config.epochs}")
    print(f"   Batch Size: {config.batch_size} (CPU-optimized)")
    print(f"   Learning Rate: {config.learning_rate}")
    print(f"   Dataset: 100% ({config.subset_ratio*100:.0f}%)")
    print(f"   Validation Split: {config.validation_split_ratio*100:.0f}%")
    print()
    print("⏱️  Estimated Time: 50-100 minutes for 20 epochs")
    print()
    print("-"*80)
    print()
    
    # Start training with progress display
    start_time = time.time()
    print("🚀 Starting training...")
    print()
    
    try:
        model_path = train(config, model_type='cnn')
        
        elapsed_time = time.time() - start_time
        minutes, seconds = divmod(int(elapsed_time), 60)
        
        print()
        print("="*80)
        print("✅ CPU Training Complete!")
        print("="*80)
        print(f"⏱️  Total Time: {minutes}m {seconds}s")
        print(f"💾 Model Saved: {model_path}")
        print(f"📊 Report: {config.model_dir / 'training_report.json'}")
        print()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Training interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error during training: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
