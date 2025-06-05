import json

with open("/home/barbara/documents/RegPatternSearch/resumo.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(type(data))
if isinstance(data, list):
    print("Exemplo de item:", data[0])
elif isinstance(data, dict):
    print("Chaves do dicionário:", data.keys())
else:
    print("Tipo inesperado:", type(data))
