from pystac_client import Client

# 1. Conecta ao catálogo
catalog = Client.open("https://data.inpe.br/bdc/stac/v1")

# 2. Período
inicio = "2025-01-01"
fim = "2025-12-31"

print(f"Buscando dados entre {inicio} e {fim}...\n")

# Dicionário para organizar os resultados
dados = {
    "AMAZONIA-1": {},
    "CBERS-4": {},
    "CBERS-4A": {}
}

# 3. Função para identificar de qual satélite é a coleção
def identificar_satelite(collection_id):
    cid = collection_id.upper()
    
    # Ordem importa: verificar CBERS-4A antes de CBERS-4 para evitar confusão
    if "CB4A" in cid or "CBERS4A" in cid:
        return "CBERS-4A"
    elif "CB4" in cid or "CBERS4" in cid: 
        return "CBERS-4"
    elif "AMZ1" in cid or "AMAZONIA1" in cid:
        return "AMAZONIA-1"
    return None

# 4. Varre todas as coleções do catálogo e filtra
for collection in catalog.get_collections():
    col_id = collection.id
    satelite = identificar_satelite(col_id)
    
    if satelite:
        try:
            # Faz a busca
            search = catalog.search(
                collections=[col_id],
                datetime=f"{inicio}/{fim}"
            )
            # Conta os itens (usando list() para forçar a contagem)
            qtd = len(list(search.items()))
            
            # Só adiciona na lista se tiver alguma imagem (para limpar o output)
            if qtd > 0:
                print(f" -> Encontrado: {col_id} ({qtd} imgs)") # Log de progresso
                dados[satelite][col_id] = qtd
                
        except Exception as e:
            print(f"Erro ao ler {col_id}: {e}")

# 5. Exibe o Relatório Final Agrupado
print("\n" + "="*50)
print(f"RELATÓRIO FINAL ({inicio} a {fim})")
print("="*50)

for satelite, colecoes in dados.items():
    print(f"\n--- {satelite} ---")
    total_satelite = 0
    
    if not colecoes:
        print(" Nenhuma imagem encontrada neste período.")
    
    # Ordena as coleções por nome para facilitar leitura
    for nome_col in sorted(colecoes.keys()):
        qtd = colecoes[nome_col]
        total_satelite += qtd
        print(f"  {nome_col:<30} : {qtd} imagens")
        
    print(f"  [TOTAL GERAL {satelite}]: {total_satelite}")

print("\n" + "="*50)