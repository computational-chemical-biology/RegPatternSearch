import os
import glob
from Bio import SeqIO
from datetime import datetime

def extrair_rRNA_16S(genbank_file, output_fasta, criar_dir=False, log_file=None):
    """
    Extrai sequências de rRNA 16S de um arquivo GenBank e salva em formato FASTA.
    Apenas considera anotações com 'product=16S ribosomal RNA' e evita duplicações
    por posição da feature.
    """

    # Verifica se o arquivo GenBank existe
    if not os.path.exists(genbank_file):
        msg = f"[ERRO] Arquivo não encontrado: {genbank_file}"
        print(msg)
        if log_file:
            with open(log_file, "a") as log:
                log.write(msg + "\n")
        return 0

    # Cria o diretório de saída, se necessário
    if criar_dir:
        pasta_saida = os.path.dirname(output_fasta)
        if pasta_saida and not os.path.exists(pasta_saida):
            os.makedirs(pasta_saida)
            print(f"[INFO] Diretório criado: {pasta_saida}")

    contador = 0
    localizacoes_extraidas = set()  # Para evitar duplicação por posição

    # Abre o GenBank para leitura e o arquivo de saída FASTA
    with open(genbank_file, "r") as gb, open(output_fasta, "w") as fasta_out:
        for record in SeqIO.parse(gb, "genbank"):
            for feature in record.features:
                if feature.type == "rRNA" and "product" in feature.qualifiers:
                    produto = feature.qualifiers["product"][0].strip().lower()
                    if produto == "16s ribosomal rna":
                        # Verifica se a localização já foi processada
                        localizacao = str(feature.location)
                        if localizacao in localizacoes_extraidas:
                            continue  # Evita duplicata
                        localizacoes_extraidas.add(localizacao)

                        # Extrai a sequência e grava no FASTA
                        seq = feature.extract(record.seq)
                        header = f">{record.id}_16S_rRNA_{localizacao}"
                        fasta_out.write(f"{header}\n{seq}\n")
                        contador += 1

    # Se nenhuma sequência foi extraída, remove o arquivo
    if contador > 0:
        msg = f"[OK] {contador} sequência(s) 16S extraída(s) de: {genbank_file}"
    else:
        msg = f"[AVISO] Nenhuma sequência 16S encontrada em: {genbank_file}"
        if os.path.exists(output_fasta):
            os.remove(output_fasta)

    print(msg)
    if log_file:
        with open(log_file, "a") as log:
            log.write(msg + "\n")

    return contador


def processar_genomas_em_subpastas(diretorio_raiz, pasta_saida="16S_resultados", log_path="log.txt"):
    """
    Varre subpastas de um diretório para encontrar arquivos GenBank (.gbff, .gbk etc),
    extrai sequências 16S, evita sobrescrever arquivos já existentes,
    e gera um log de execução detalhado.
    """

    total_arquivos = 0
    total_ignorados = 0
    total_16S = 0

    # Cria ou zera o arquivo de log
    with open(log_path, "w") as log:
        log.write(f"=== LOG DE EXTRAÇÃO DE rRNA 16S ===\n")
        log.write(f"Início: {datetime.now()}\n\n")

    # Procura arquivos GenBank (.gbff, .gbk, .gb etc) recursivamente
    arquivos_genbank = glob.glob(os.path.join(diretorio_raiz, '**', '*.gb*'), recursive=True)

    for caminho_completo in arquivos_genbank:
        total_arquivos += 1

        # Cria nome único: nome da pasta pai + nome do arquivo
        pasta_pai = os.path.basename(os.path.dirname(caminho_completo))
        arquivo_nome = os.path.splitext(os.path.basename(caminho_completo))[0]
        nome_base = f"{pasta_pai}_{arquivo_nome}"

        # Define caminho do arquivo de saída
        saida_fasta = os.path.join(pasta_saida, f"{nome_base}_16S.fasta")

        # Ignora se o arquivo de saída já existe
        if os.path.exists(saida_fasta):
            msg = f"[IGNORADO] Já existe: {saida_fasta}"
            print(msg)
            with open(log_path, "a") as log:
                log.write(msg + "\n")
            total_ignorados += 1
            continue

        # Executa a extração do arquivo atual
        num_16S = extrair_rRNA_16S(
            caminho_completo,
            saida_fasta,
            criar_dir=True,
            log_file=log_path
        )

        total_16S += num_16S

    # Registra o resumo final no log
    with open(log_path, "a") as log:
        log.write(f"\n=== RESUMO FINAL ===\n")
        log.write(f"Total de arquivos encontrados: {total_arquivos}\n")
        log.write(f"Arquivos ignorados (já existiam): {total_ignorados}\n")
        log.write(f"Total de sequências 16S extraídas: {total_16S}\n")
        log.write(f"Fim: {datetime.now()}\n")
        log.write(f"===============================\n")


def main():
    # Diretório onde estão os arquivos GenBank
    diretorio_raiz = '/home/barbara/documents/RegPatternSearch/ncbi_dataset/data'
    # Pasta de saída dos arquivos FASTA
    pasta_saida = "16S_resultados"
    # Arquivo de log
    log_path = "log.txt"

    processar_genomas_em_subpastas(diretorio_raiz, pasta_saida, log_path)


if __name__ == "__main__":
    main()
