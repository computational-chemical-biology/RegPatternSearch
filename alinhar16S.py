import os
import subprocess
from Bio import SeqIO

def concatenate_fasta(fasta_dir, output_fasta):
    """
    Função para concatenar arquivos FASTA em um único arquivo.
    - Abre e lê todos os arquivos .fasta no diretório fornecido.
    - Escreve as sequências em um arquivo de saída único.
    """
    # Lista todos os arquivos FASTA no diretório
    fasta_files = [os.path.join(fasta_dir, filename) for filename in os.listdir(fasta_dir) if filename.endswith('.fasta')]

    # Abre o arquivo de saída para escrever as sequências concatenadas
    with open(output_fasta, "w") as output_file:
        for fasta_file in fasta_files:
            # Abre cada arquivo FASTA individualmente
            with open(fasta_file, "r") as input_file:
                # Escreve o conteúdo do arquivo FASTA no arquivo de saída
                output_file.write(input_file.read())

    # Mensagem de confirmação após gerar o arquivo concatenado
    print(f"Arquivo concatenado gerado: {output_fasta}")

def align_sequences_with_mafft(input_fasta, output_fasta):
    """
    Função para alinhar sequências usando o MAFFT.
    - Chama o MAFFT através da linha de comando.
    - Gera um arquivo de saída com as sequências alinhadas.
    """
    # Comando para rodar o MAFFT usando a opção --auto, que ajusta automaticamente os parâmetros do alinhamento
    mafft_command = f"mafft --auto {input_fasta} > {output_fasta}"
    
    # Executa o comando MAFFT via subprocess
    subprocess.run(mafft_command, shell=True, check=True)
    
    # Mensagem de confirmação após gerar o arquivo alinhado
    print(f"Sequências alinhadas geradas: {output_fasta}")

def main():
    """
    Função principal que coordena a execução do processo:
    - Concatenar arquivos FASTA.
    - Alinhar as sequências com MAFFT.
    """
    # Caminho para o diretório onde os arquivos FASTA estão armazenados
    fasta_dir = "/home/barbara/documents/RegPatternSearch/16S_resultados"

    # Caminho para o arquivo de saída que vai armazenar todas as sequências concatenadas
    concatenated_fasta = "/home/barbara/documents/RegPatternSearch/all_sequences.fasta"
    
    # Caminho para o arquivo de saída onde as sequências alinhadas serão salvas
    aligned_fasta = "/home/barbara/documents/RegPatternSearch/aligned_sequences.fasta"

    # Passo 1: Concatenar as sequências de todos os arquivos FASTA no diretório
    concatenate_fasta(fasta_dir, concatenated_fasta)

    # Passo 2: Alinhar as sequências concatenadas usando o MAFFT
    align_sequences_with_mafft(concatenated_fasta, aligned_fasta)

# Garantir que o código dentro de main() seja executado apenas quando o script for rodado diretamente
if __name__ == "__main__":
    main()

