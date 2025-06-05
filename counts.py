import json
import re
from collections import Counter

#Path to the JSON file
arquivo = "/home/barbara/documents/RegPatternSearch/resumo.json"

def extrair_genero_especie(nome):
    #Extract only the genus and species (first two words)
    match = re.match(r"^([A-Za-z]+ [a-z]+)", nome)
    if match:
        return match.group(1)
    return nome

#Load the JSON file
with open(arquivo, "r", encoding="utf-8") as f:
    dados = json.load(f)

contador_especies = Counter()

#Iterate through each record in the 'reports' list
for registro in dados.get("reports", []):
    #Try to get the species name from average_nucleotide_identity
    nome_completo = registro.get("average_nucleotide_identity", {}).get("submitted_organism")
    if not nome_completo:
        #Fallback to using the organism name from the 'organism' field
        nome_completo = registro.get("organism", {}).get("organism_name")
    if nome_completo:
        #Clean and normalize the name, remove brackets and extract genus + species
        especie = extrair_genero_especie(nome_completo.strip().replace('[', '').replace(']', ''))
        contador_especies[especie] += 1

#Print the five most frequent species
print("\nTop 5 most frequent species:")
for especie, contagem in contador_especies.most_common(5):
    print(f"{especie}: {contagem}")

#Specific count for a known species - only for test
print(f"\nCount of 'Streptomyces avermitilis': {contador_especies.get('Streptomyces avermitilis', 0)}")
print(f"\nCount of 'Streptomyces microflavus': {contador_especies.get('Streptomyces microflavus', 0)}")

#Total number of genomes analyzed
print(f"\nTotal number of genomes analyzed: {sum(contador_especies.values())}")
