import csv, json

def export_to_csv(dados, name):
    """Exports data to a CSV file."""
    nome_arquivo = name + ".csv"
    chaves = ["Nota", "Comentario"]
    with open(nome_arquivo, 'w', newline='') as arquivo_csv:
        escritor_csv = csv.DictWriter(arquivo_csv, fieldnames=chaves)
        escritor_csv.writeheader()
        for linha in dados:
            escritor_csv.writerow(linha)
    print("Dados exportados para", nome_arquivo)

def export_to_json(dados, name):
    """Exports data to a JSON file."""
    nome_arquivo = name + ".json"
    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo_json:
        json.dump(dados, arquivo_json, ensure_ascii=False, indent=4)
    print("Dados exportados para", nome_arquivo)