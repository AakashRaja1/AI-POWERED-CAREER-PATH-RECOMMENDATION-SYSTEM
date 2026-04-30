#!/usr/bin/env python
"""
Start GPU training once PyTorch CUDA is ready
"""
import subprocess
import sys
import time

def check_gpu():
    """Check if GPU PyTorch is available"""
    try:
        import torch
        cuda_available = torch.cuda.is_available()
        cuda_version = torch.version.cuda
        return cuda_available, cuda_version
    except ImportError:
        return False, None

def main():
    print("="*70)
    print("GPU PYTORCH TRAINER LAUNCHER")
    print("="*70)
    
    while True:
        cuda_available, cuda_version = check_gpu()
        
        if cuda_available:
            print(f"✓ GPU PyTorch Ready!")
            print(f"✓ CUDA Version: {cuda_version}")
            print("="*70)
            print("Starting CNN personality model training on GPU...")
            print("="*70)
            print()
            
            # Start training
            result = subprocess.run(
                [sys.executable, "backend/ml_personality_pipeline/gpu_train_optimal.py"],
                cwd="."
            )
            sys.exit(result.returncode)
        else:
            print("⏳ GPU PyTorch still installing...")
            print("   Downloading PyTorch CUDA 12.4 (2.5 GB)")
            print("   Checking again in 30 seconds...")
            time.sleep(30)

if __name__ == "__main__":
    main()
