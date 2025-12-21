#!/bin/bash
#SBATCH --job-name=langchain
#SBATCH --partition=mediumq
#SBATCH --gres=gpu:h100_2g.24gb:1
#SBATCH --qos=mediumq
#SBATCH --output=logs/langchain_output_%j.log
#SBATCH --cpus-per-task=1
#SBATCH --mem=5G

# Load Conda environment
source ~/.bashrc
conda init
conda activate langchain


# Run the test script
python /home/scratch-scholars/Abrar/LangChain/2.ChatModels/5_1_chatmodel_hf_local.py
