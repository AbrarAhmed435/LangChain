#!/bin/bash
#SBATCH --job-name=langchain
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

python /home/gaash/Wasif/Abrar/Personal/LangChain/3.EmbedingModels/7_RAG_01.py