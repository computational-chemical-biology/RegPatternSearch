import json
import re
from collections import Counter
import matplotlib.pyplot as plt  # Import for plotting

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
top5 = contador_especies.most_common(5)
print("\nTop 5 most frequent species:")
for especie, contagem in top5:
    print(f"{especie}: {contagem}")

#Specific count for a known species - only for test
print(f"\nCount of 'Streptomyces avermitilis': {contador_especies.get('Streptomyces avermitilis', 0)}")
print(f"\nCount of 'Streptomyces microflavus': {contador_especies.get('Streptomyces microflavus', 0)}")

#Total number of genomes analyzed
print(f"\nTotal number of genomes analyzed: {sum(contador_especies.values())}")

#Create a bar chart of the top 5 most frequent species
especies = [item[0] for item in top5]
contagens = [item[1] for item in top5]

plt.figure(figsize=(10, 6))
plt.bar(especies, contagens, color='skyblue')
plt.title('Top 5 Most Frequent Streptomyces Species')
plt.xlabel('Species')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

#Save the figure and show it
plt.savefig("top5_species_barplot.png")  # Saves the plot as a PNG file
plt.show()  # Displays the plot interactively
