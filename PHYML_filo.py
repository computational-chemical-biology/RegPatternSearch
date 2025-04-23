import os
import subprocess
from Bio import SeqIO
from ete3 import TreeStyle, PhyloTree

# Caminho para o diretório com subpastas contendo arquivos .faa
input_dir = "/home/barbara/documents/RegPatternSearch/ncbi_dataset/data"

# Caminho onde os arquivos FASTA com 16S rRNA serão salvos
output_dir = "/home/barbara/documents/RegPatternSearch/16S_sequences_from_faa"
os.makedirs(output_dir, exist_ok=True)  # Cria o diretório de saída se não existir

# Caminho para os diretórios de saída do alinhamento e árvore filogenética
aligned_output_dir = "/home/barbara/documents/RegPatternSearch/aligned_16S"
tree_output_dir = "/home/barbara/documents/RegPatternSearch/trees"
os.makedirs(aligned_output_dir, exist_ok=True)
os.makedirs(tree_output_dir, exist_ok=True)

# Limite para teste: número máximo de arquivos .faa a processar
max_files = 10
count = 0

print(f"\n🔍 Buscando arquivos .faa em: {input_dir}")
print(f"📂 Processando até {max_files} arquivos...\n")

# Função para extrair sequências 16S rRNA de um arquivo .faa
def extract_16S_from_faa(faa_path, output_path):
    output_records = []
    
    # Percorrer o arquivo .faa
    with open(faa_path, "r") as handle:
        for record in SeqIO.parse(handle, "fasta"):
            # Verifica se a descrição do cabeçalho contém "16S"
            if "16S" in record.description:
                # Adiciona a sequência ao arquivo de saída
                fasta_record = f">{record.id}\n{record.seq}\n"
                output_records.append(fasta_record)

    # Se houver sequências 16S, salva no arquivo de saída
    if output_records:
        with open(output_path, "w") as out_f:
            out_f.writelines(output_records)
        print(f"✅ Sequências 16S salvas em: {output_path}")
    else:
        print(f"⚠️ Nenhuma sequência 16S encontrada em: {faa_path}")

# Função para alinhar as sequências com MAFFT
def align_sequences_with_mafft(fasta_file, aligned_output):
    with open(aligned_output, "w") as outfile:
        subprocess.run(["mafft", "--auto", fasta_file], stdout=outfile)
    print(f"✅ Sequências alinhadas e salvas em: {aligned_output}")

# Função para construir a árvore filogenética com PhyML
def build_phyml_tree(aligned_fasta, tree_output):
    subprocess.run(["phyml", "-i", aligned_fasta, "-d", "nt", "-b", "1000", "-m", "GTR"])
    tree_file = f"{aligned_fasta}_phyml_tree.txt"
    os.rename(tree_file, tree_output)
    print(f"✅ Árvore filogenética gerada e salva em: {tree_output}")

# Função para visualizar a árvore filogenética
def visualize_tree(tree_file):
    if os.path.exists(tree_file) and os.path.getsize(tree_file) > 0:
        tree = PhyloTree(tree_file)
        ts = TreeStyle()
        ts.title.add_face("Árvore Filogenética 16S", column=0)
        ts.show_leaf_name = True
        tree.show(tree_style=ts)
    else:
        print("🚨 Erro: Arquivo de árvore não encontrado ou está vazio.")

# Percorre todas as subpastas procurando arquivos .faa
for root, dirs, files in os.walk(input_dir):
    for file in files:
        if file.endswith(".faa"):
            if count >= max_files:
                break

            faa_path = os.path.join(root, file)
            base_name = os.path.splitext(file)[0]
            output_fasta = os.path.join(output_dir, f"{base_name}_16S.fasta")

            print(f"🔍 [{count+1}] Processando: {faa_path}")
            extract_16S_from_faa(faa_path, output_fasta)
            count += 1

    if count >= max_files:
        break

print(f"\n✅ Finalizado! Total de arquivos .faa processados: {count}")
print(f"📁 Sequências 16S salvas em: {output_dir}")
