from Bio import AlignIO, Phylo
import subprocess
import matplotlib.pyplot as plt
import os

def convert_fasta_to_phylip(fasta_path, phylip_path):
    """Convert alignment from FASTA to PHYLIP-relaxed format."""
    alignment = AlignIO.read(fasta_path, "fasta-pearson")
    AlignIO.write(alignment, phylip_path, "phylip-relaxed")

def run_phyml(phylip_path):
    """Run PhyML on the PHYLIP file with 100 bootstraps."""
    cmd = ["phyml", "-i", phylip_path, "-d", "nt", "-b", "100"]
    subprocess.run(cmd, check=True)

def visualize_tree(tree_file):
    """Display phylogenetic tree using Biopython and Matplotlib."""
    tree = Phylo.read(tree_file, "newick")
    Phylo.draw(tree)

def main():
    """Main workflow: convert, run PhyML, and visualize tree."""
    fasta_path = "/home/barbara/documents/RegPatternSearch/aligned_sequences.fasta"
    phylip_path = "/home/barbara/documents/RegPatternSearch/aligned_sequences.phy"
    
    print("Converting to PHYLIP...")
    convert_fasta_to_phylip(fasta_path, phylip_path)

    print("Running PhyML...")
    run_phyml(phylip_path)

    tree_file = phylip_path + "_phyml_tree.txt"

    if os.path.exists(tree_file):
        print("Displaying tree...")
        visualize_tree(tree_file)
    else:
        print(f"Tree file not found: {tree_file}")

if __name__ == "__main__":
    main()

