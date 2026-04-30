#!/usr/bin/env python
"""
CPU Training Launcher with Live Progress Display
Trains the personality CNN model on CPU with real-time progress monitoring
"""
import subprocess
import sys
import os

def main():
    print("\n" + "="*80)
    print(" " * 20 + "🖥️  CPU PERSONALITY CNN TRAINING 🖥️")
    print("="*80)
    print()
    print("📦 Installing dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "tqdm", "-q"], check=False)
    
    print("✅ Ready to train!")
    print()
    print("="*80)
    print(" " * 15 + "STARTING TRAINING WITH LIVE PROGRESS")
    print("="*80)
    print()
    
    # Start training
    result = subprocess.run(
        [sys.executable, "backend/ml_personality_pipeline/train_cpu.py"],
        cwd="."
    )
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
