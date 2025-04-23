import os
import subprocess
from ete3 import TreeStyle, PhyloTree

# Função para extrair sequência 16S rRNA usando Barrnap
def extract_16S_from_fna(fna_file, output_dir):
    # Gera um nome base para o arquivo a partir do nome do genoma
    base_name = os.path.basename(fna_file).replace(".fna", "")
    fasta_file = os.path.join(output_dir, f"{base_name}_16S.fasta")

    # Executa o Barrnap com a opção --outseq para salvar as sequências diretamente em fasta
    subprocess.run(["barrnap", "--kingdom", "bac", "--outseq", fasta_file, fna_file])

    return fasta_file  # Retorna o caminho do arquivo fasta gerado

# Função para alinhar as sequências usando MAFFT
def align_sequences_with_mafft(fasta_file, aligned_output):
    #Executa MAFFT e redireciona a saída para o arquivo alinhado
    subprocess.run(["mafft", "--auto", fasta_file], stdout=open(aligned_output, "w"))

# Função para construir a árvore filogenética com PhyML
def build_phyml_tree(aligned_fasta, tree_output):
    #Executa PhyML com modelo GTR, dados do tipo nucleotídeo e 1000 bootstraps
    subprocess.run(["phyml", "-i", aligned_fasta, "-d", "nt", "-b", "1000", "-m", "GTR"])
    
    #Renomeia a árvore gerada pelo PhyML para um nome mais amigável
    os.rename(f"{aligned_fasta}_phyml_tree.txt", tree_output)

#Função para visualizar a árvore com ETE3
def visualize_tree(tree_file):
    if os.path.exists(tree_file) and os.path.getsize(tree_file) > 0:
        tree = PhyloTree(tree_file)
        ts = TreeStyle()
        ts.title.add_face("Árvore Filogenética 16S", column=0)
        ts.show_leaf_name = True
        tree.show(tree_style=ts)
    else:
        print("🚨 Erro: Arquivo de árvore não encontrado ou está vazio.")

#Verifica se um arquivo está vazio
def is_file_empty(file_path):
    return not os.path.exists(file_path) or os.stat(file_path).st_size == 0

#Diretórios principais
input_dir = "/home/barbara/documents/RegPatternSearch/genomas_baixados"
output_dir = "/home/barbara/documents/RegPatternSearch/16S_sequences"
aligned_output_dir = os.path.join(output_dir, "aligned")
tree_output_dir = os.path.join(output_dir, "trees")

#Arquivos de saída finais
combined_fasta = os.path.join(output_dir, "all_16S_combined.fasta")
aligned_fasta = os.path.join(aligned_output_dir, "aligned_16S.fasta")
tree_file = os.path.join(tree_output_dir, "tree_16S.nwk")

#Criação dos diretórios de saída, se necessário
for directory in [output_dir, aligned_output_dir, tree_output_dir]:
    os.makedirs(directory, exist_ok=True)

#Lista que guardará os arquivos fasta extraídos
all_fasta_files = []

#LIMITAR o número de arquivos .fna para teste (por exemplo, 10)
max_files = 10
count = 0
done = False

print(f"\n🔍 Procurando arquivos .fna em: {input_dir}")
print(f"📂 Máximo de arquivos a processar: {max_files}\n")

# Percorre recursivamente o diretório de entrada e processa os primeiros 10 arquivos .fna encontrados
for root, dirs, files in os.walk(input_dir):
    for file in files:
        if file.endswith(".fna"):
            if count >= max_files:
                done = True
                break

            fna_path = os.path.join(root, file)
            print(f"✅ [{count + 1}] Processando: {fna_path}")
            fasta = extract_16S_from_fna(fna_path, output_dir)

            # Só adiciona se o arquivo fasta realmente existir e não estiver vazio
            if os.path.exists(fasta) and os.path.getsize(fasta) > 0:
                all_fasta_files.append(fasta)
                count += 1
            else:
                print(f"⚠️  Arquivo {fasta} vazio ou inexistente. Ignorando.")

    if done:
        break

#Lista os arquivos processados
print("\n📄 Arquivos .fna utilizados no teste:")
for i, fna in enumerate(all_fasta_files, 1):
    print(f"  {i:02d} ➜ {fna}")

#Combina todas as sequências fasta extraídas em um único arquivo
if all_fasta_files:
    with open(combined_fasta, "w") as outfile:
        for fasta_file in all_fasta_files:
            with open(fasta_file, "r") as infile:
                outfile.write(infile.read())
else:
    print("\n❌ Nenhum arquivo de sequência 16S válido foi gerado. Encerrando script.")
    exit()

# Alinha as sequências com MAFFT
print("\n🧬 Alinhando sequências com MAFFT...")
align_sequences_with_mafft(combined_fasta, aligned_fasta)

# Verifica se o alinhamento deu certo antes de prosseguir
if is_file_empty(aligned_fasta):
    print("❌ Arquivo de alinhamento está vazio. Encerrando script.")
    exit()

# Constrói a árvore filogenética com PhyML
print("\n🌳 Construindo árvore filogenética com PhyML...")
build_phyml_tree(aligned_fasta, tree_file)

# Visualiza a árvore
print("\n👀 Visualizando árvore gerada...")
visualize_tree(tree_file)
