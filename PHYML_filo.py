# o 16S extraído ainda está errado pois pega o rRNA 16S pelo gff como produto e não desconsidera quando é uma enzima relacionada
import os
import subprocess
from glob import glob
from pathlib import Path
from ete3 import Tree, TreeStyle  # Para visualizar a árvore filogenética gerada

# Função para extrair a sequência 16S de um arquivo genômico .fna usando um arquivo GFF existente
def extract_16S_from_existing_gff(fna_file, gff_file, output_dir):
    """
    Extrai a sequência 16S de um arquivo genômico .fna usando um arquivo GFF existente.
    """
    base_name = os.path.basename(fna_file).replace(".fna", "")  # Extrai o nome base do arquivo .fna (sem extensão)
    fasta_file = os.path.join(output_dir, f"{base_name}_16S.fasta")  # Caminho do arquivo de saída para a sequência 16S extraída

    # Processar o GFF e pegar as coordenadas do gene 16S
    with open(gff_file, 'r') as gff:
        for line in gff:
            if line.startswith("#"):  # Ignorar linhas de comentário
                continue

            # Filtrar pela característica "rRNA" e o tipo "16S"
            fields = line.strip().split("\t")  # Divide a linha do GFF em campos
            feature_type = fields[2]  # Tipo de feature (como gene, rRNA, etc.)
            if feature_type != "rRNA":  # Só considerar genes do tipo rRNA
                continue

            attributes = fields[8]  # Atributos da linha, geralmente contém o nome do gene
            if "16S" not in attributes:  # Filtra pela presença de "16S" no nome do gene
                continue  # Ignora se não for gene 16S

            start = int(fields[3])  # Posição inicial do gene 16S no arquivo
            end = int(fields[4])  # Posição final do gene 16S no arquivo
            strand = fields[6]  # Sentido da transcrição (pode ser + ou -)

            # Extrair a sequência correspondente do arquivo .fna
            with open(fna_file, 'r') as fna:
                seq = ""  # Inicializa a sequência genômica
                for fna_line in fna:
                    if fna_line.startswith(">"):  # Ignora linhas de descrição
                        continue
                    seq += fna_line.strip()  # Concatena todas as linhas de sequência

                # Pegar a sequência do gene 16S
                gene_sequence = seq[start-1:end]  # Extrai a sequência do gene 16S (ajustando o índice)
                if strand == "-":  # Se a transcrição for no sentido negativo, faz o complemento reverso
                    gene_sequence = reverse_complement(gene_sequence)

                # Salvar no arquivo fasta
                with open(fasta_file, 'a') as output_fasta:
                    output_fasta.write(f">{base_name}_16S\n{gene_sequence}\n")  # Salva no formato FASTA

# Função para gerar a sequência complementar reversa
def reverse_complement(sequence):
    """
    Retorna a sequência complementar reversa de uma sequência de DNA.
    """
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}  # Mapa de complementos de bases
    return ''.join(complement.get(base, base) for base in reversed(sequence))  # Reverte a sequência e aplica o complemento

# Função para alinhar múltiplos arquivos fasta com MAFFT
def align_sequences_with_mafft(input_fastas_pattern, aligned_output):
    """
    Alinha as sequências 16S com MAFFT.
    """
    # Coletar todos os arquivos fasta
    fasta_files = glob(input_fastas_pattern)  # Padrão de entrada para buscar arquivos fasta
    
    # Concatenar todos os arquivos fasta em um único arquivo temporário
    combined_fasta = "combined_16S_temp.fasta"  # Arquivo temporário para combinar as sequências
    with open(combined_fasta, "w") as outfile:
        for fasta in fasta_files:
            with open(fasta, "r") as infile:
                outfile.write(infile.read())  # Escreve cada arquivo fasta no arquivo combinado
    
    # Executar MAFFT para alinhar as sequências
    subprocess.run(["mafft", "--auto", combined_fasta], stdout=open(aligned_output, "w"), check=True)
    
    # Remover arquivo temporário
    os.remove(combined_fasta)  # Apaga o arquivo temporário após o alinhamento

# Função para construir a árvore filogenética com PhyML
def build_phyml_tree(aligned_fasta, tree_output):
    """
    Constrói a árvore filogenética usando PhyML.
    """
    subprocess.run(["phyml", "-i", aligned_fasta, "-d", "nt", "-b", "1000", "-m", "GTR"], check=True)
    os.rename(f"{aligned_fasta}_phyml_tree.txt", tree_output)  # Renomeia o arquivo gerado para o nome de saída

# Função para visualizar a árvore com ETE3
def visualize_tree(tree_file):
    """
    Visualiza a árvore filogenética gerada.
    """
    tree = Tree(tree_file)  # Carrega a árvore filogenética gerada
    ts = TreeStyle()  # Estilo para exibir a árvore
    ts.title.add_face("Árvore Filogenética 16S", column=0)  # Adiciona título à árvore
    ts.show_leaf_name = True  # Exibe os nomes das folhas
    tree.show(tree_style=ts)  # Exibe a árvore com o estilo definido

# Função principal para executar o pipeline completo
def main():
    """
    Função principal que orquestra todo o pipeline:
    1. Extrai as sequências 16S
    2. Alinha as sequências
    3. Constrói a árvore filogenética
    4. Visualiza a árvore
    """
    # Coletar até 4 arquivos .fna das subpastas
    fna_files = sorted(glob("genomas_baixados/ncbi_dataset/data/*/.fna", recursive=True))[:4]

    # Verifica se há arquivos .fna encontrados
    if len(fna_files) == 0:
        print("Nenhum arquivo .fna encontrado nas subpastas de 'genomas_baixados/ncbi_dataset/data/'.")
        return
    elif len(fna_files) < 4:
        print(f"Atenção: apenas {len(fna_files)} arquivos encontrados. Continuando com o que há.")

    output_dir = "results/16S_sequences"  # Diretório de saída para as sequências 16S
    aligned_output = "results/aligned_16S.fasta"  # Arquivo de saída para o alinhamento
    tree_output = "results/tree_16S.nwk"  # Arquivo de saída para a árvore filogenética

    os.makedirs(output_dir, exist_ok=True)  # Cria o diretório de saída, se não existir

    # Extrair sequências 16S de cada arquivo .fna
    for fna_file in fna_files:
        # Procurar qualquer arquivo .gff ou .gff.gz na mesma pasta
        fna_path = Path(fna_file)
        possible_gffs = list(fna_path.parent.glob(".gff"))  # Procura arquivos GFF na pasta

        if not possible_gffs:  # Se não encontrar GFF correspondente, ignora o arquivo .fna
            print(f"GFF correspondente não encontrado para {fna_file}, pulando.")
            continue

        gff_file = str(possible_gffs[0])  # Usa o primeiro arquivo GFF encontrado
        extract_16S_from_existing_gff(fna_file, gff_file, output_dir)  # Extrai a sequência 16S

    # Verificar se há sequências extraídas antes de alinhar
    fasta_check = glob(os.path.join(output_dir, "*_16S.fasta"))  # Verifica se há arquivos FASTA de 16S
    if not fasta_check:  # Se não houver, aborta o processo
        print("Nenhuma sequência 16S foi extraída. Abortando alinhamento e construção da árvore.")
        return

    # Alinhar sequências 16S extraídas
    align_sequences_with_mafft(os.path.join(output_dir, "*_16S.fasta"), aligned_output)

    # Construir árvore filogenética a partir do alinhamento
    build_phyml_tree(aligned_output, tree_output)

    # Visualizar a árvore gerada
    visualize_tree(tree_output)

# Executar o script
if __name__ == "__main__":  # Verifica se o script está sendo executado diretamente
    main()  # Chama a função principal para rodar todo o pipeline
