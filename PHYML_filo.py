import os
import subprocess
from ete3 import Tree, TreeStyle

# Função para extrair as sequências 16S de arquivos .fna com Barrnap
def extract_16S_from_fna(fna_file, output_dir):
    """
    Extrai a sequência 16S de um arquivo genômico .fna usando Barrnap.
    """
    base_name = os.path.basename(fna_file).replace(".fna", "")
    gff_file = os.path.join(output_dir, f"{base_name}_rRNA.gff")
    fasta_file = os.path.join(output_dir, f"{base_name}_16S.fasta")
    
    # Rodar Barrnap
    subprocess.run(["barrnap", "--kingdom", "bac", f"--output", gff_file, f"--fasta", fna_file])

    # Filtrar as sequências 16S
    with open(gff_file, "r") as gff:
        with open(fasta_file, "w") as fasta:
            for line in gff:
                if "16S_rRNA" in line:
                    fields = line.strip().split("\t")
                    sequence = fields[-1]
                    fasta.write(f">{sequence}\n{sequence}\n")
                    
    return fasta_file

# Função para alinhar as sequências 16S com MAFFT
def align_sequences_with_mafft(fasta_file, aligned_output):
    """
    Alinha as sequências 16S com MAFFT.
    """
    subprocess.run(["mafft", "--auto", fasta_file], stdout=open(aligned_output, "w"))

# Função para construir a árvore filogenética com PhyML
def build_phyml_tree(aligned_fasta, tree_output):
    """
    Constrói a árvore filogenética usando PhyML.
    """
    # PhyML executando a análise
    subprocess.run(["phyml", "-i", aligned_fasta, "-d", "nt", "-b", "1000", "-m", "GTR"])

    # Renomeia o arquivo gerado pelo PhyML
    os.rename(f"{aligned_fasta}_phyml_tree", tree_output)

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

# Caminho para os arquivos de entrada
fna_files = ["genomas/genoma1.fna", "genomas/genoma2.fna"]  # Exemplos de arquivos .fna
output_dir = "results/16S_sequences"
aligned_output = "results/aligned_16S.fasta"
tree_output = "results/tree_16S.nwk"

# Etapa 1: Extrair as sequências 16S
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for fna_file in fna_files:
    extract_16S_from_fna(fna_file, output_dir)

# Etapa 2: Alinhar as sequências 16S
align_sequences_with_mafft("results/16S_sequences/*_16S.fasta", aligned_output)

# Etapa 3: Construir a árvore filogenética com PhyML
build_phyml_tree(aligned_output, tree_output)

# Etapa 4: Visualizar a árvore
visualize_tree(tree_output)
