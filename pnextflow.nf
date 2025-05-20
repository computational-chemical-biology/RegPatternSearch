nextflow.enable.dsl = 2

params.base_dir = '/temporario2/9877294/extracted_gbff'
params.output_base = '/temporario2/9877294/Resultados_AntiSMASH'

workflow {

    arquivos_ch = Channel
        .fromPath("${params.base_dir}/*_genomic.gbff")
        .map { arquivo -> 
            tuple(arquivo.getBaseName().replace('_genomic.gbff', ''), arquivo)
        }
        .take(6)

    runAntismash(arquivos_ch)
}

process runAntismash {

    tag { genoma_name }

    input:
    tuple val(genoma_name), path(arquivo)

    output:
    path "${genoma_name}_antismash", dir: true, emit: antismash_out

    publishDir "${params.output_base}", mode: 'copy'

    script:
    """
    mkdir -p ${genoma_name}_antismash
    antismash --genefinding-tool prodigal "$arquivo" --output-dir ${genoma_name}_antismash
    """
}