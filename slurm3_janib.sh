#!/bin/bash
#SBATCH --job-name=langchain
#SBATCH --partition=mediumq
#SBATCH --qos=mediumq
#SBATCH --nodelist=gpu1
#SBATCH --gres=gpu:h100_2g.24gb:1
#SBATCH --cpus-per-task=1
#SBATCH --mem=5G
#SBATCH --output=logs/langchain_output_%j.log

# Load CUDA module (optional, but fine)
module load cuda/12.9

# Proper conda activation (NO conda init)
source /apps/anaconda3/etc/profile.d/conda.sh
conda activate langchain

echo "CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"
nvidia-smi

# IMPORTANT: use srun
srun python /home/scratch-scholars/Abrar/LangChain/3.EmbedingModels/4_document_embedding.py

