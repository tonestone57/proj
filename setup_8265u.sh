#!/bin/bash
# Authoritative setup process for Intel i5-8265U (SGI Standard)

echo "Initializing SGI Environment for Intel Core i5-8265U..."

# 1. Environment Variables for 4-thread limit
export OMP_NUM_THREADS=4
export MKL_NUM_THREADS=4
export OPENBLAS_NUM_THREADS=4
export VECLIB_MAXIMUM_THREADS=4
export NUMEXPR_NUM_THREADS=4
export KMP_BLOCKTIME=1
export PYTHONDONTWRITEBYTECODE=1

# 2. Dependency Installation
echo "Installing/Updating core dependencies..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install --pre --upgrade ipex-llm[all]
pip install ray psutil pyyaml z3-solver lancedb tree-sitter

# 3. Path Setup
export PYTHONPATH=$PYTHONPATH:$(pwd)

echo "Environment Configured. Ready for SGI-Alpha execution."
