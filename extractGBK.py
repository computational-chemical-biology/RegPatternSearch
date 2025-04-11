import glob
import shutil
import os

def extract_gbk_files(source_dir, target_dir):
    # Expande o caminho com ~ para o diretório home do usuário
    source_dir = os.path.expanduser(source_dir)
    
    # Cria o diretório de destino, se ele não existir
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # Padrão glob para encontrar todos os arquivos .gbk em subpastas
    gbk_files = glob.glob(os.path.join(source_dir, '**', '*.gbk'), recursive=True)

    # Para cada arquivo .gbk encontrado
    for file in gbk_files:
        # Nome do arquivo sem o caminho
        filename = os.path.basename(file)
        
        # Caminho de destino para o arquivo copiado
        target_file = os.path.join(target_dir, filename)
        
        try:
            # Copia o arquivo .gbk para o diretório de destino
            shutil.copy(file, target_file)
            print(f"Arquivo {filename} extraído com sucesso para {target_dir}")
        except Exception as e:
            print(f"Erro ao copiar o arquivo {filename}: {e}")

if __name__ == "__main__":
    # Caminho de origem com ~, apontando para a pasta de saída do Prokka
    source_directory = '~/documents/RegPatternSearch/prokka_output'  # Ajuste conforme necessário

    # Diretório onde os arquivos .gbk serão armazenados
    target_directory = './extracted_gbk'  # Ajuste conforme necessário

    # Executa a função para extrair os arquivos .gbk
    extract_gbk_files(source_directory, target_directory)
