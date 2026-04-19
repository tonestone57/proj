#!/bin/bash
# SGI Roadmap: Intel CPU Acceleration Setup
# Targeted for: Intel Core i5-8265U (Whiskey Lake)

# 1. Create a dedicated Conda environment
# conda create -n sgi-env python=3.11 -y
# source activate sgi-env

# 2. Install Intel-optimized PyTorch and IPEX-LLM
# Using CPU-specific wheels for AVX2 optimization on 8265U
pip install --pre --upgrade ipex-llm[all] \
    --extra-index-url https://download.pytorch.org/whl/cpu

# 3. Install Ray for Distributed Actor Management
pip install "ray[default]"

# 4. Install SGI Roadmap dependencies
pip install psutil transformers==4.36.2 omegaconf pandas lancedb sentence-transformers pyyaml

# 5. Set Runtime Environment Variables
# Ensures correct thread management for 8265U (4 Cores / 8 Threads)
echo "export OMP_NUM_THREADS=8" >> ~/.bashrc
echo "export KMP_BLOCKTIME=1" >> ~/.bashrc
# source ~/.bashrc

echo "✅ SGI Environment Ready. Use 'conda activate sgi-env' to start the Hub."
