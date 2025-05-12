#!/bin/bash -f
#SBATCH --partition=SP2
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=20
#SBATCH -J antismash_dsl2
#SBATCH --time=10:00:00

# Ativa o ambiente Conda (ajuste conforme necessário)
source /temporario2/9877294/anaconda3/etc/profile.d/conda.sh
conda activate

# Diretórios base
base_dir="/temporario2/9877294/ncbi_dataset/data"
output_base="/temporario2/9877294/Resultados_AntiSMASH"

mkdir -p logs

# Cria o pipeline DSL2
cat > pnextflow.nf << 'EOF'
nextflow.enable.dsl = 2

params.base_dir = '/temporario2/9877294/ncbi_dataset/data'
params.output_base = '/temporario2/9877294/Resultados_AntiSMASH'

workflow {

    arquivos_ch = Channel
        .fromPath("${params.base_dir}/**/genomic.gbff")
        .map { arquivo -> tuple(arquivo.getParent().getName(), arquivo) }

    runAntismash(arquivos_ch)
}

process runAntismash {

    tag { genoma_name }

    input:
    tuple val(genoma_name), path(arquivo)

    output:
    path "${genoma_name}_antismash", emit: antismash_out

    script:
    """
    mkdir -p ${genoma_name}_antismash
    antismash --genefinding-tool prodigal \\
              --relaxed \\
              "$arquivo" \\
              --output-dir ${genoma_name}_antismash
    """
}
EOF

# Cria o arquivo de configuração para execução no SLURM
cat > nextflow.config << 'EOF'
process.executor = 'slurm'

process {
    cpus = 20
    memory = '32 GB'
    time = '40h'
    queue = 'SP2'
}

executor {
    queueSize = 100
    submitRateLimit = '1 sec'
}
EOF

# Roda o pipeline
nextflow run pnextflow.nf -resume \
    -with-report report.html \
    -with-trace trace.txt \
    -with-timeline timeline.html \
    -with-dag flowchart.png
