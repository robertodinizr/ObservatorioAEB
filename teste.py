from pystac_client import Client

catalog = Client.open("https://data.inpe.br/bdc/stac/v1")

inicio = "2025-01-01"
fim = "2025-12-31"

print(f"Buscando dados entre {inicio} e {fim}...\n")

dados = {
    "AMAZONIA-1": {},
    "CBERS-4": {},
    "CBERS-4A": {}
}

def identificar_satelite(collection_id):
    cid = collection_id.upper()

    if "CB4A" in cid or "CBERS4A" in cid:
        return "CBERS-4A"
    elif "CB4" in cid or "CBERS4" in cid: 
        return "CBERS-4"
    elif "AMZ1" in cid or "AMAZONIA1" in cid:
        return "AMAZONIA-1"
    return None

for collection in catalog.get_collections():
    col_id = collection.id
    satelite = identificar_satelite(col_id)
    
    if satelite:
        try:
            search = catalog.search(
                collections=[col_id],
                datetime=f"{inicio}/{fim}"
            )
            qtd = len(list(search.items()))
            
            if qtd > 0:
                print(f" -> Encontrado: {col_id} ({qtd} imgs)")
                dados[satelite][col_id] = qtd
                
        except Exception as e:
            print(f"Erro ao ler {col_id}: {e}")

print("\n" + "="*50)
print(f"RELATÓRIO FINAL ({inicio} a {fim})")
print("="*50)

for satelite, colecoes in dados.items():
    print(f"\n--- {satelite} ---")
    total_satelite = 0
    
    if not colecoes:
        print(" Nenhuma imagem encontrada neste período.")
    
    for nome_col in sorted(colecoes.keys()):
        qtd = colecoes[nome_col]
        total_satelite += qtd
        print(f"  {nome_col:<30} : {qtd} imagens")
        
    print(f"  [TOTAL GERAL {satelite}]: {total_satelite}")

print("\n" + "="*50)