from pystac_client import Client

catalog = Client.open("https://data.inpe.br/bdc/stac/v1")

print("Coleções disponíveis:")
for collection in catalog.get_collections():
    print(f" - {collection.id}")