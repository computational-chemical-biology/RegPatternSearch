#!/bin/bash -f
#SBATCH --job-name=antismash_nextflow
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=20
#SBATCH --mem=32G
#SBATCH --time=48:00:00
#SBATCH --output=nextflow_%j.out 
#SBATCH --error=nextflow_%j.err

# Ativa o Conda
source /temporario2/9877294/anaconda3/etc/profile.d/conda.sh
conda activate

# Executa a pipeline Nextflow
nextflow run pnextflow.nf -resume \
    -with-report report.html \
    -with-trace trace.txt \
    -with-timeline timeline.html \
    -with-dag dag.png

# Criar pasta de logs, se necessário
mkdir -p logs

