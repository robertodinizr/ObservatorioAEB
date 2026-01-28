from pystac_client import Client

catalog = Client.open("https://data.inpe.br/bdc/stac/v1")

inicio = "2025-01-01"
fim = "2025-12-31"

target_collections = [
    "AMZ1-WFI-L2-DN-1",
    "AMZ1-WFI-L4-DN-1",
    
    "CB4A-MUX-L2-DN-1",
    "CB4A-MUX-L4-DN-1",
    "CB4A-WFI-L2-DN-1",
    "CB4A-WFI-L4-DN-1",
    "CB4A-WPM-L2-DN-1",
    "CB4A-WPM-L4-DN-1",
    
    "CB4-WFI-L2-DN-1",
    "CB4-WFI-L4-DN-1",
    "CB4-MUX-L2-DN-1",
    "CB4-MUX-L4-DN-1",
    "CB4-PAN10M-L4-DN-1",
    "CB4-PAN10M-L2-DN-1",
    "CB4-PAN5M-L2-DN-1",
    "CB4-PAN5M-L4-DN-1"
]

print(f"Buscando dados entre {inicio} e {fim} nas bases selecionadas...\n")

dados = {
    "AMAZONIA-1": 0,
    "CBERS-4": 0,
    "CBERS-4A": 0
}

def identificar_satelite(collection_id):
    cid = collection_id.upper()
    if "CB4A" in cid: return "CBERS-4A"
    if "CB4" in cid: return "CBERS-4"
    if "AMZ1" in cid: return "AMAZONIA-1"
    return "OUTROS"

print(f"{'COLEÇÃO':<30} | {'QTD'}")
print("-" * 40)

for col_id in target_collections:
    try:
        search = catalog.search(
            collections=[col_id],
            datetime=f"{inicio}/{fim}"
        )
        qtd = len(list(search.items()))
        
        print(f"{col_id:<30} | {qtd}")
        
        sat = identificar_satelite(col_id)
        if sat in dados:
            dados[sat] += qtd
            
    except Exception as e:
        print(f"Erro ao buscar {col_id}: {e}")

print("\n" + "="*40)
print(f"RESUMO FINAL (Soma L2 + L4)")
print("="*40)
for sat, total in dados.items():
    print(f"{sat:<15}: {total} imagens")