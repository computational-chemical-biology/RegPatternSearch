import os
import subprocess
from ete3 import TreeStyle, PhyloTree

# Função para extrair apenas sequências 16S rRNA de arquivos .fna usando barrnap
def extract_16S_from_fna(fna_file, output_dir):
    base_name = os.path.basename(fna_file).replace(".fna", "")  # Extrai o nome do arquivo base
    full_output = os.path.join(output_dir, f"{base_name}_rRNAs.fasta")  # Nome temporário do arquivo de saída

    # Executa o barrnap para extrair rRNAs do arquivo .fna
    result = subprocess.run(
        ["barrnap", "--kingdom", "bac", "--outseq", full_output, fna_file],
        capture_output=True, text=True
    )

    # Arquivo para salvar somente as sequências 16S extraídas
    filtered_output = os.path.join(output_dir, f"{base_name}_16S.fasta")

    # Verifica se o arquivo com todas as rRNAs foi criado
    if os.path.exists(full_output):
        with open(full_output, "r") as infile, open(filtered_output, "w") as outfile:
            write = False
            for line in infile:
                if line.startswith(">"):
                    write = "16S" in line  # Somente escrever se for 16S
                if write:
                    outfile.write(line)
        os.remove(full_output)  # Remove o arquivo temporário com todos os rRNAs
        return filtered_output if os.path.exists(filtered_output) else None
    else:
        return None

# Função para alinhar as sequências com MAFFT
def align_sequences_with_mafft(input_fasta, output_fasta):
    with open(output_fasta, "w") as outfile:
        subprocess.run(["mafft", "--auto", input_fasta], stdout=outfile)

# Função para construir árvore filogenética com PhyML
def build_phyml_tree(aligned_fasta):
    subprocess.run(["phyml", "-i", aligned_fasta, "-d", "nt", "-b", "1000", "-m", "GTR"])

# Função para visualizar árvore com ETE3
def visualize_tree(tree_file):
    if os.path.exists(tree_file) and os.path.getsize(tree_file) > 0:
        tree = PhyloTree(tree_file)
        ts = TreeStyle()
        ts.title.add_face("Árvore Filogenética 16S", column=0)
        ts.show_leaf_name = True
        tree.show(tree_style=ts)
    else:
        print("🚨 Erro: Arquivo de árvore não encontrado ou está vazio.")

# Caminhos principais
input_dir = "/home/barbara/documents/RegPatternSearch/genomas_baixados/ncbi_dataset/data"
output_dir = "/home/barbara/documents/RegPatternSearch/16S_sequences_from_fna"
aligned_dir = "/home/barbara/documents/RegPatternSearch/aligned_16S"
tree_file_path = os.path.join(aligned_dir, "aligned_16S.fasta_phyml_tree.txt")
combined_fasta = os.path.join(aligned_dir, "aligned_16S.fasta")

# Criação dos diretórios de saída, se não existirem
os.makedirs(output_dir, exist_ok=True)
os.makedirs(aligned_dir, exist_ok=True)

# Coleta até 10 arquivos .fna com 16S válidos
all_fasta = []
max_files = 10
count = 0

print(f"\n🔍 Buscando arquivos .fna em: {input_dir}")
print(f"📂 Processando até {max_files} arquivos...\n")

for root, _, files in os.walk(input_dir):
    for file in files:
        if file.endswith(".fna") and count < max_files:
            fna_path = os.path.join(root, file)
            print(f"➡️ Processando: {fna_path}")
            fasta_16S = extract_16S_from_fna(fna_path, output_dir)
            if fasta_16S and os.path.exists(fasta_16S) and os.path.getsize(fasta_16S) > 0:
                all_fasta.append(fasta_16S)
                count += 1

print(f"\n✅ Finalizado! Total de arquivos .fna processados: {count}")
print(f"📁 Sequências 16S salvas em: {output_dir}")

# Combina todas as sequências FASTA extraídas em um único arquivo
if all_fasta:
    with open(combined_fasta, "w") as outfile:
        for fasta in all_fasta:
            with open(fasta, "r") as infile:
                outfile.write(infile.read())
else:
    print("❌ Nenhum arquivo FASTA válido foi extraído.")
    exit()

# Alinhamento com MAFFT
print("\n🧬 Alinhando sequências com MAFFT...")
align_sequences_with_mafft(combined_fasta, combined_fasta)

# Construção da árvore com PhyML
print("\n🌳 Construindo árvore filogenética com PhyML...")
build_phyml_tree(combined_fasta)

# Visualização da árvore gerada
print("\n👀 Visualizando árvore gerada...")
visualize_tree(tree_file_path)
