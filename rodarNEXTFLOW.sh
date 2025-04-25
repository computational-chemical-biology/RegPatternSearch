#!/bin/bash
#SBATCH --job-name=antismash_nextflow
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=48:00:00
#SBATCH --output=nextflow_%j.out 
#SBATCH --error=nextflow_%j.err

##AJUSTAR PARAMETROS ACIMA ^

module load nextflow
nextflow run main.nf -resume
