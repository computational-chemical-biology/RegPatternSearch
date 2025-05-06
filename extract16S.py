import os
import glob
from Bio import SeqIO
from datetime import datetime

## NOTA DE PROBLEMA: ele filtra os 16S mas pega as proteinas relacionadas ao 16S ainda

# Função para extrair sequências de rRNA 16S de um único arquivo GenBank
def extrair_rRNA_16S(genbank_file, output_fasta, criar_dir=False, log_file=None):
    """
    Extrai sequências de rRNA 16S de um arquivo GenBank e salva em FASTA.
    Também registra as ações em um arquivo de log, se fornecido.
    Retorna o número de sequências extraídas.
    """

    # Verifica se o arquivo de entrada existe
    if not os.path.exists(genbank_file):
        msg = f"[ERRO] Arquivo não encontrado: {genbank_file}"
        print(msg)
        # Escreve o erro no log, se fornecido
        if log_file:
            with open(log_file, "a") as log:
                log.write(msg + "\n")
        return 0  # Retorna 0 pois não houve extração

    # Cria o diretório do arquivo de saída, se necessário e se solicitado
    if criar_dir:
        pasta_saida = os.path.dirname(output_fasta)
        if pasta_saida and not os.path.exists(pasta_saida):
            os.makedirs(pasta_saida)  # Cria a pasta
            print(f"[INFO] Diretório criado: {pasta_saida}")

    contador = 0  # Inicializa contador de sequências 16S encontradas

    # Abre o arquivo GenBank para leitura e o arquivo de saída para escrita
    with open(genbank_file, "r") as gb, open(output_fasta, "w") as fasta_out:
        # Itera por cada registro (genoma) presente no arquivo
        for record in SeqIO.parse(gb, "genbank"):
            # Itera por cada feature anotada no genoma
            for feature in record.features:
                # Verifica se a feature é um rRNA com anotação 'product'  ##O erro possivelmente está aqui
                if feature.type == "rRNA" and "product" in feature.qualifiers:
                    # Verifica se o produto é "16S ribosomal RNA"
                    produto = feature.qualifiers["product"][0].lower()
                    if "16s ribosomal rna" in produto:
                        # Extrai a sequência correspondente à feature
                        seq = feature.extract(record.seq)
                        # Cria um cabeçalho FASTA com o ID e localização
                        header = f">{record.id}_16S_rRNA_{feature.location}"
                        # Escreve o cabeçalho e a sequência no arquivo de saída
                        fasta_out.write(f"{header}\n{seq}\n")
                        contador += 1  # Incrementa o contador

    # Gera mensagem com base no número de sequências extraídas
    if contador > 0:
        msg = f"[OK] {contador} sequência(s) 16S extraída(s) de: {genbank_file}"
    else:
        msg = f"[AVISO] Nenhuma sequência 16S encontrada em: {genbank_file}"
        # Remove arquivo de saída vazio, se não extraiu nada
        if os.path.exists(output_fasta):
            os.remove(output_fasta)

    # Exibe a mensagem no terminal
    print(msg)
    # Escreve a mensagem no log, se fornecido
    if log_file:
        with open(log_file, "a") as log:
            log.write(msg + "\n")

    return contador  # Retorna o número de sequências encontradas


#Função para percorrer várias subpastas e processar arquivos GenBank automaticamente
def processar_genomas_em_subpastas(diretorio_raiz, pasta_saida="16S_resultados", log_path="log.txt"):
    """
    Percorre recursivamente todas as subpastas de `diretorio_raiz`,
    identifica arquivos GenBank (.gb/.gbk), extrai rRNA 16S,
    salva em arquivos FASTA e registra tudo em log.txt.
    """

    # Inicializa contadores para estatísticas do log
    total_arquivos = 0        # Total de arquivos .gb/.gbk encontrados
    total_ignorados = 0       # Arquivos ignorados porque já foram processados
    total_16S = 0             # Total de sequências 16S extraídas

    # Cria/limpa o arquivo de log e escreve cabeçalho com data e hora
    with open(log_path, "w") as log:
        log.write(f"=== LOG DE EXTRAÇÃO DE rRNA 16S ===\n")
        log.write(f"Início: {datetime.now()}\n\n")

    # Usa glob para buscar todos os arquivos .gb e .gbk recursivamente
    arquivos_genbank = glob.glob(os.path.join(diretorio_raiz, '**', '*.gb*'), recursive=True)

    ## caminho teste: /home/barbara/documents/RegPatternSearch/genomas_baixados/ncbi_dataset/dados

    # Itera sobre os arquivos encontrados
    for caminho_completo in arquivos_genbank:
        total_arquivos += 1  # Conta o arquivo

        # Remove extensão para usar como base do nome de saída
        nome_base = os.path.splitext(os.path.basename(caminho_completo))[0]

        # Define caminho de saída na pasta de resultados
        saida_fasta = os.path.join(pasta_saida, f"{nome_base}_16S.fasta")

        # Se o arquivo de saída já existe, ignora e registra no log
        if os.path.exists(saida_fasta):
            msg = f"[IGNORADO] Já existe: {saida_fasta}"
            print(msg)
            with open(log_path, "a") as log:
                log.write(msg + "\n")
            total_ignorados += 1  # Conta como ignorado
            continue  # Pula para o próximo arquivo

        # Chama a função de extração e obtém o número de sequências extraídas
        num_16S = extrair_rRNA_16S(
            caminho_completo,
            saida_fasta,
            criar_dir=True,
            log_file=log_path
        )

        # Soma ao total geral de sequências 16S
        total_16S += num_16S

    # Ao final do processamento, escreve um resumo no log
    with open(log_path, "a") as log:
        log.write(f"\n=== RESUMO FINAL ===\n")
        log.write(f"Total de arquivos encontrados: {total_arquivos}\n")
        log.write(f"Arquivos ignorados (já existiam): {total_ignorados}\n")
        log.write(f"Total de sequências 16S extraídas: {total_16S}\n")
        log.write(f"Fim: {datetime.now()}\n")
        log.write(f"===============================\n")


# Função principal para rodar o script
def main():
    """
    Função principal que chama o processo de extração e geração de log.
    """
    diretorio_raiz = "genomas"  # Defina o caminho para a pasta com os genomas
    pasta_saida = "16S_resultados"  # Defina o diretório de saída para os arquivos FASTA
    log_path = "log.txt"  # Defina o arquivo de log

    # Chama a função de processamento de genomas
    processar_genomas_em_subpastas(diretorio_raiz, pasta_saida, log_path)


# Execução do script
if __name__ == "__main__":
    main()
