import os
import subprocess
from glob import glob
from ete3 import Tree, TreeStyle

# Função para extrair a sequência 16S de um único arquivo .fna usando Barrnap
def extract_16S_from_fna(fna_file, output_dir):
    """
    Extrai a sequência 16S de um arquivo genômico .fna usando Barrnap.
    """
    base_name = os.path.basename(fna_file).replace(".fna", "")
    gff_file = os.path.join(output_dir, f"{base_name}_rRNA.gff")
    fasta_file = os.path.join(output_dir, f"{base_name}_16S.fasta")

    # Rodar Barrnap
    subprocess.run(["barrnap", "--kingdom", "bac", "--outseq", fasta_file, fna_file], check=True)

    return fasta_file

# Função para alinhar múltiplos arquivos fasta com MAFFT
def align_sequences_with_mafft(input_fastas_pattern, aligned_output):
    """
    Alinha as sequências 16S com MAFFT.
    """
    # Coletar todos os arquivos fasta
    fasta_files = glob(input_fastas_pattern)
    
    # Concatenar todos os arquivos fasta em um único arquivo temporário
    combined_fasta = "combined_16S_temp.fasta"
    with open(combined_fasta, "w") as outfile:
        for fasta in fasta_files:
            with open(fasta, "r") as infile:
                outfile.write(infile.read())
    
    # Executar MAFFT
    subprocess.run(["mafft", "--auto", combined_fasta], stdout=open(aligned_output, "w"), check=True)
    
    # Remover arquivo temporário
    os.remove(combined_fasta)

# Função para construir a árvore filogenética com PhyML
def build_phyml_tree(aligned_fasta, tree_output):
    """
    Constrói a árvore filogenética usando PhyML.
    """
    subprocess.run(["phyml", "-i", aligned_fasta, "-d", "nt", "-b", "1000", "-m", "GTR"], check=True)
    os.rename(f"{aligned_fasta}_phyml_tree.txt", tree_output)

# Função para visualizar a árvore com ETE3
def visualize_tree(tree_file):
    """
    Visualiza a árvore filogenética gerada.
    """
    tree = Tree(tree_file)
    ts = TreeStyle()
    ts.title.add_face("Árvore Filogenética 16S", column=0)
    ts.show_leaf_name = True
    tree.show(tree_style=ts)

# Função principal para executar o pipeline completo
def main():
    fna_files = ["genomas/genoma1.fna", "genomas/genoma2.fna"]  # Substituir pelos caminhos corretos
    output_dir = "results/16S_sequences"
    aligned_output = "results/aligned_16S.fasta"
    tree_output = "results/tree_16S.nwk"

    # Criar diretório de saída, se necessário
    os.makedirs(output_dir, exist_ok=True)

    # Etapa 1: Extrair sequências 16S
    for fna_file in fna_files:
        extract_16S_from_fna(fna_file, output_dir)

    # Etapa 2: Alinhar sequências
    align_sequences_with_mafft(os.path.join(output_dir, "*_16S.fasta"), aligned_output)

    # Etapa 3: Construir árvore filogenética
    build_phyml_tree(aligned_output, tree_output)

    # Etapa 4: Visualizar árvore
    visualize_tree(tree_output)

# Executar o script
if __name__ == "__main__":
    main()
