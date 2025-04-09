import glob
import shutil
import os

def extract_fna_files(source_dir, target_dir):
    # Expande o caminho com ~ para o diretório home do usuário
    source_dir = os.path.expanduser(source_dir)
    
    # Cria o diretório de destino, se ele não existir
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # Padrão glob para encontrar todos os arquivos .fna em subpastas
    fna_files = glob.glob(os.path.join(source_dir, '**', '*.fna'), recursive=True)

    # Para cada arquivo .fna encontrado
    for file in fna_files:
        # Nome do arquivo sem o caminho, apenas o nome do arquivo
        filename = os.path.basename(file)
        
        # Caminho para onde o arquivo será copiado
        target_file = os.path.join(target_dir, filename)
        
        try:
            # Copia o arquivo .fna para o diretório de destino
            shutil.copy(file, target_file)
            print(f"Arquivo {filename} extraído com sucesso para {target_dir}")
        except Exception as e:
            print(f"Erro ao copiar o arquivo {filename}: {e}")

if __name__ == "__main__":
    # Caminho com ~ para o diretório onde os dados estão localizados (pasta DATA)
    source_directory = '~/documents/RegPatternSearch/genomas_baixados/ncbi_dataset/data'  # Ajuste conforme necessário
    
    # Diretório onde os arquivos .fna serão armazenados
    target_directory = './extracted_fna'  # Ajuste conforme necessário
    
    # Chama a função para extrair os arquivos .fna
    extract_fna_files(source_directory, target_directory)
