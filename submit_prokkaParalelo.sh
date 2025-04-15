#!/bin/bash
#SBATCH --job-name=prokka_parallel
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=08:00:00
#SBATCH --output=prokka_%j.out
#SBATCH --error=prokka_%j.err

# Ativa o Conda do miniconda3 (onde está o prokka)
source /temporario2/9877294/miniconda3/etc/profile.d/conda.sh
conda activate base

# Executa o script de paralelização
./run_prokka_parallel.sh
