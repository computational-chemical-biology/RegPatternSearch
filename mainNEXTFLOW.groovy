#ainda será testado e adaptado

params.input = "data/genomas/*.fasta"
params.outdir = "resultados"

process ANTISMASH {
    tag "$arquivo_genoma.simpleName"

    input:
    path arquivo_genoma

    output:
    path "${arquivo_genoma.simpleName}" dir: true into saidas

    script:
    """
    mkdir -p ${arquivo_genoma.simpleName}
    ./scripts/run_antismash.sh $arquivo_genoma ${arquivo_genoma.simpleName}
    """
}

process PARSE_RESULTADOS {
    input:
    path saidas.collect()

    output:
    path "resultados_final.tsv"

    script:
    """
    python3 scripts/parse_antismash.py
    """
}

workflow {
    arquivos = Channel.fromPath(params.input)
    ANTISMASH(arquivos)
    PARSE_RESULTADOS(saidas)
}
