#!/bin/bash
#SBATCH --job-name=langchain
#SBATCH --partition=mediumq
#SBATCH --gres=gpu:h100_1g.24gb:1
#SBATCH --nodelist=gpu1
#SBATCH --qos=mediumq
#SBATCH --output=logs/langchain_output_%j.log
#SBATCH --cpus-per-task=1
#SBATCH --mem=5G

##### CUDA MODULE
module purge
#module load cuda/12.9

# Load Conda environment
#source ~/.bashrc
#conda init
#oconda activate langchain
source /apps/anaconda3/etc/profile.d/conda.sh
conda activate langchain

echo "HOSTNAME=$(hostname)"
echo "CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"


# Run the test script
# python /home/scratch-scholars/Abrar/LangChain/2.ChatModels/5_1_chatmodel_hf_local.py
python /home/scratch-scholars/Abrar/LangChain/3.EmbedingModels/5_document_similarity.py
#srun --gpu-bind=single:1 python testing_gpu_on_janib.py

