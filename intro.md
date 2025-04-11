## Introdução

Para o download dos genomas, é necessário instalar a ferramenta de download do NCBI.

As ferramentas de linha de comando do NCBI Datasets estão disponíveis como um pacote Conda que inclui tanto `datasets` quanto `dataformat`.

---

## Instalação da ferramenta de download do NCBI

1. Crie um novo ambiente Conda:

    ```bash
    conda create -n ncbi_datasets
    ```

2. Ative o novo ambiente:

    ```bash
    conda activate ncbi_datasets
    ```

3. Instale o pacote `ncbi-datasets-cli`:

    ```bash
    conda install -c conda-forge ncbi-datasets-cli
    ```

---

## Download dos Genomas

Você pode utilizar o seguinte comando para baixar um genoma específico pelo taxon ID (exemplo: 1883):

```bash
./datasets download genome taxon 1883 --annotated --reference --include genome,protein
```
ou utilizar a função *download_genomas.py*

---

## Organização dos Arquivos

Cada genoma baixado terá um subdiretório onde os arquivos .faa, .fna, .gff, entre outros, estarão presentes.

Para a próxima etapa (com a ferramenta Prokka), será necessário utilizar apenas os arquivos .fna. Para isso, usamos a função em python *extractFNA.py*, que extrai e organiza esses arquivos em uma única pasta.

##### Script Bash para extrair arquivos .fna
```bash
#!/bin/bash

# Caminho de origem com $HOME expandido para o diretório home do usuário
source_directory="$HOME/documents/RegPatternSearch/genomas_baixados/ncbi_dataset/data"

# Diretório de destino para onde os arquivos .fna serão copiados
target_directory="./extracted_fna"

# Cria o diretório de destino se não existir
mkdir -p "$target_directory"

# Comando find para procurar arquivos .fna e copiá-los para o diretório de destino
find "$source_directory" -type f -name "*.fna" -exec cp {} "$target_directory" \;

echo "Arquivos .fna extraídos para $target_directory"`
```

---
## Ferramenta Prokka
### Instalação do Prokka

A ferramenta Prokka pode ser instalada via Conda com o seguinte comando:
```bash
conda install -c conda-forge -c bioconda -c defaults prokka
```
#### Instalação do Barrnap (Requisito)

Após instalar o Prokka, também é necessário instalar o barrnap, que é utilizado por ele. É importante verificar a versão para garantir compatibilidade:

```bash
conda install -c bioconda -c conda-forge barrnap
```
### Execução do Prokka
A linha de comando padrão para rodar o Prokka em é:

```bash
prokka /pastadoarquivo/arquivo.fna
```

Como o arquivo de interesse é o .fna, utilizamos os arquivos previamente extraídos e reunidos em uma pasta para rodar o Prokka:

```bash
for file in /home/barbara/documents/RegPatternSearch/extracted_fna/*.fna; do
  dir_name=$(basename "$file" .fna)
  output_dir="/home/barbara/documents/RegPatternSearch/prokka_output/$dir_name"
  prokka --prefix "$dir_name" --outdir "$output_dir" "$file"
done
```

Este script executa o Prokka para cada arquivo .fna presente na pasta extracted_fna, criando uma saída separada para cada genoma em /prokka_output.

---

## Ferramenta AntiSMASH
### Instalação do AntiSMASH

Para instalar a ferramenta antiSMASH 

```bash
conda create -n antismash antismash
conda activate antismash
download-antismash-databases
conda deactivate
```
Como arquivos de entrada utilizaremos os arquivos .gbk gerados pela ferramenta de anotação Prokka anteriormente.

Linha de comando padrão:

```bash
conda activate antismash
antismash arquivodeentrada.gbk
```
