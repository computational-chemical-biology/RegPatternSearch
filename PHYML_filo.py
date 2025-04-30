import os
import subprocess
from glob import glob
from Bio import SeqIO
from ete3 import Tree, TreeStyle

# -------------------------------
# Função para extrair 16S de arquivos GFF + FNA
# -------------------------------
def extract_16S_from_existing_gff(fna_file, gff_file, output_dir):
    """
    Extrai sequências 16S rRNA com base em um GFF já existente.
    """
    base_name = os.path.basename(fna_file).replace(".fna", "")
    fasta_file = os.path.join(output_dir, f"{base_name}_16S.fasta")

    # Carregar genoma
    seq_records = SeqIO.to_dict(SeqIO.parse(fna_file, "fasta"))

    # Abrir GFF e extrair apenas regiões 16S
    with open(gff_file, "r") as gff_in, open(fasta_file, "w") as fasta_out:
        for line in gff_in:
            if line.startswith("#"):
                continue
            fields = line.strip().split("\t")
            if len(fields) > 8 and "16S" in fields[8]:
                seq_id = fields[0]
                start = int(fields[3])
                end = int(fields[4])
                strand = fields[6]

                # Extrair sequência
                seq = seq_records[seq_id].seq[start - 1:end]
                if strand == "-":
                    seq = seq.reverse_complement()

                fasta_out.write(f">{base_name}_{seq_id}_{start}_{end}_16S\n{seq}\n")

    return fasta_file

# -------------------------------
# Função para alinhar as sequências 16S com MAFFT
# -------------------------------
def align_sequences_with_mafft(input_fastas_pattern, aligned_output):
    """
    Alinha as sequências 16S com MAFFT.
    """
    from glob import glob

    fasta_files = glob(input_fastas_pattern)
    combined_fasta = "combined_16S_temp.fasta"

    with open(combined_fasta, "w") as outfile:
        for fasta in fasta_files:
            with open(fasta, "r") as infile:
                outfile.write(infile.read())

    subprocess.run(["mafft", "--auto", combined_fasta], stdout=open(aligned_output, "w"), check=True)
    os.remove(combined_fasta)

# -------------------------------
# Função para construir a árvore filogenética com PhyML
# -------------------------------
def build_phyml_tree(aligned_fasta, tree_output, num_threads=4):
    """
    Constrói a árvore filogenética usando PhyML.
    """
    os.environ["OMP_NUM_THREADS"] = str(num_threads)

    subprocess.run(["phyml", "-i", aligned_fasta, "-d", "nt", "-b", "1000", "-m", "GTR"], check=True)
    os.rename(f"{aligned_fasta}_phyml_tree.txt", tree_output)

# -------------------------------
# Função para visualizar a árvore com ETE3
# -------------------------------
def visualize_tree(tree_file):
    """
    Visualiza a árvore filogenética gerada.
    """
    tree = Tree(tree_file)
    ts = TreeStyle()
    ts.title.add_face("Árvore Filogenética 16S", column=0)
    ts.show_leaf_name = True
    tree.show(tree_style=ts)

# -------------------------------
# Função principal
# -------------------------------
from glob import glob

def main():
    # Caminho para buscar .fna em subpastas
    fna_files = sorted(glob("genomas_baixados/ncbi_dataset/data/**/*.fna", recursive=True))[:10]

    if len(fna_files) == 0:
        print("Nenhum arquivo .fna encontrado nas subpastas de 'genomas_baixados/ncbi_dataset/data/'.")
        return
    elif len(fna_files) < 10:
        print(f"Atenção: apenas {len(fna_files)} arquivos encontrados. Continuando com o que há.")

    output_dir = "results/16S_sequences"
    aligned_output = "results/aligned_16S.fasta"
    tree_output = "results/tree_16S.nwk"

    os.makedirs(output_dir, exist_ok=True)

    for fna_file in fna_files:
        gff_file = fna_file.replace(".fna", ".gff")
        if not os.path.exists(gff_file):
            print(f"GFF correspondente não encontrado para {fna_file}, pulando.")
            continue

        extract_16S_from_existing_gff(fna_file, gff_file, output_dir)

    align_sequences_with_mafft(os.path.join(output_dir, "*_16S.fasta"), aligned_output)
    build_phyml_tree(aligned_output, tree_output)
    visualize_tree(tree_output)


# -------------------------------
# Executar o pipeline
# -------------------------------
if __name__ == "__main__":
    main()
