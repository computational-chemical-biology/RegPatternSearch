params.base_dir = '/temporario2/9877294/ncbi_dataset/data'
params.output_base = '/temporario2/9877294/Resultados_AntiSMASH'

// Busca todos os arquivos .gbff em subdiretórios
Channel
    .fromPath("${params.base_dir}/**/genomic.gbff")
    .set { arquivos }

process runAntismash {
    tag "${genoma_name}"

    input:
    path arquivo from arquivos

    output:
    path "${genoma_name}_antismash"

    when:
    // Só executa se o diretório de saída ainda não existir
    !file("${genoma_name}_antismash").exists()

    script:
    genome_dir = arquivo.toString().tokenize('/')[-2]
    genoma_name = genome_dir

    """
    mkdir -p ${genoma_name}_antismash
    antismash --genefinding-tool prodigal \\
              --relaxed \\
              "$arquivo" \\
              --output-dir ${genoma_name}_antismash
    """
}

