#!/bin/bash -f
#SBATCH --partition=SP2
#SBATCH --ntasks=1              # numero de CPUs - neste exemplo, 1 CPU
#SBATCH --cpus-per-task=1       # Number OpenMP Threads per process
#SBATCH -J aloca-1-cpu
#SBATCH --time=10:00:00         # Se voce nao especificar, o default é 8 horas. O limite é 480 horas

# Caminho para os arquivos .fna
input_dir="/temporario2/9877294/extracted_fna"
output_base="/temporario2/9877294/prokka_output"

# Número de jobs em paralelo (ajuste de acordo com SLURM)
JOBS=4

# Roda prokka em paralelo para cada .fna
parallel --jobs $JOBS '
  file={};
  dir_name=$(basename "$file" .fna);
  output_dir="'$output_base'/$dir_name";
  mkdir -p "$output_dir";
  prokka --prefix "$dir_name" --outdir "$output_dir" "$file"
' ::: "$input_dir"/*.fna
