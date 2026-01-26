from pystac_client import Client

catalog = Client.open("https://data.inpe.br/bdc/stac/v1")

def contar_imagens(collection_id, inicio, fim):
    search = catalog.search(
        collections=[collection_id],
        datetime=f"{inicio}/{fim}"
    )
    return sum(1 for _ in search.items())

inicio = "2021-01-01"
fim = "2025-12-31"

colecoes = {
    "AMAZONIA-1": ["AMAZONIA-1_WFI"],
    "CBERS-4": ["CBERS-4_MUX", "CBERS-4_PAN10M"],
    "CBERS-4A": ["CBERS-4A_WPM", "CBERS-4A_MUX"]
}

for missao, sensores in colecoes.items():
    total = 0
    for s in sensores:
        qtd = contar_imagens(s, inicio, fim)
        print(f"{s}: {qtd}")
        total += qtd
    print(f"➡️ TOTAL {missao}: {total} imagens\n")