#!/usr/bin/

// Definindo os parâmetros de entrada e saída
params.base_dir = '/temporario2/9877294/ncbi_dataset/data'
params.output_base = '/temporario2/9877294/Resultados_AntiSMASH'

// Definindo o canal que busca todos os arquivos genomic.gbff em subdiretórios
Channel
    .fromPath("${params.base_dir}/**/genomic.gbff")
    .set { arquivos }

// Definindo o processo para rodar o antiSMASH
process runAntismash {
    input:
    path arquivo from arquivos

    output:
    path "${genoma_name}_antismash" // Resultados serão salvos em um diretório baseado no nome do genoma

    script:
    """
    genome_dir = arquivo.toString().tokenize('/')[-2] // Extrai o nome do diretório pai (genoma)
    genoma_name = genome_dir // Define o nome do genoma

    mkdir -p ${genoma_name}_antismash // Cria o diretório de saída para armazenar os resultados

    antismash --genefinding-tool prodigal \\
              --relaxed \\
              "$arquivo" \\
              --output-dir ${genoma_name}_antismash // Executa o antiSMASH para cada genoma
    """
}

// Definindo o workflow que orquestra o processo
workflow {
    // Chamando o processo para rodar o antiSMASH nos arquivos encontrados
    runAntismash()
}
