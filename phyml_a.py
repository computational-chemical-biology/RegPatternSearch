from Bio import AlignIO, Phylo
import subprocess
import matplotlib.pyplot as plt
import os

def convert_fasta_to_phylip(fasta_path, phylip_path):
    """Converte um alinhamento de FASTA para PHYLIP-relaxed."""
    # Lê o arquivo FASTA e converte para PHYLIP-relaxed
    alignment = AlignIO.read(fasta_path, "fasta-pearson")  # ou "fasta-blast"
    AlignIO.write(alignment, phylip_path, "phylip-relaxed")  # Usando 'phylip-relaxed' para nomes maiores

def run_phyml(phylip_path):
    """Executa o PhyML no arquivo PHYLIP especificado."""
    cmd = ["phyml", "-i", phylip_path, "-d", "nt", "-b", "100"]
    subprocess.run(cmd, check=True)

def visualize_tree(tree_file):
    """Visualiza a árvore filogenética usando Biopython e Matplotlib."""
    tree = Phylo.read(tree_file, "newick")
    Phylo.draw(tree)

def main():
    # Caminhos
    fasta_path = "/home/barbara/documents/RegPatternSearch/aligned_sequences.fasta"
    phylip_path = "/home/barbara/documents/RegPatternSearch/aligned_sequences.phy"
    
    # Etapas do processo
    print("Convertendo arquivo FASTA para PHYLIP...")
    convert_fasta_to_phylip(fasta_path, phylip_path)

    print("Executando PhyML...")
    run_phyml(phylip_path)

    # Nome padrão do arquivo de saída gerado pelo PhyML
    tree_file = phylip_path + "_phyml_tree.txt"

    if os.path.exists(tree_file):
        print("Visualizando a árvore filogenética...")
        visualize_tree(tree_file)
    else:
        print(f"Arquivo de árvore não encontrado: {tree_file}")

if __name__ == "__main__":
    main()

