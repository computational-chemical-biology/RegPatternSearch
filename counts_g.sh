#!/bin/bash

python3 - <<EOF
import json
import re
from collections import Counter

arquivo = "/temporario2/9877294/ncbi_dataset/data/assembly_data_report.jsonl"

def extrair_genero_especie(nome):
    # Extrai só o gênero e a espécie (as duas primeiras palavras)
    match = re.match(r"^([A-Za-z]+ [a-z]+)", nome)
    if match:
        return match.group(1)
    return nome

contador_especies = Counter()

with open(arquivo, "r", encoding="utf-8") as f:
    for linha in f:
        registro = json.loads(linha)
        nome_completo = registro.get("averageNucleotideIdentity", {}).get("submittedOrganism")
        if not nome_completo:
            nome_completo = registro.get("organism", {}).get("organismName")
        if nome_completo:
            especie = extrair_genero_especie(nome_completo.strip())
            contador_especies[especie] += 1

print("\nContagem das 5 espécies mais frequentes:")
for especie, contagem in contador_especies.most_common(5):
    print(f"{especie}: {contagem}")