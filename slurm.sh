#!/bin/bash
#SBATCH --job-name=sam3
#SBATCH --partition=highq
#SBATCH --gres=gpu:h100:1
#SBATCH --qos=highq
#SBATCH --output=logs/abrar_output_%j.log
#SBATCH --cpus-per-task=8
#SBATCH --mem=200G
#SBATCH --time=3-00:00:00

# 1. Load Environment
source ~/.bashrc
conda activate langchain

python /home/gaash/Wasif/Abrar/Personal/LangChain/2.ChatModels/5_1_chatmodel_hf_local.py