import requests
from pprint import pprint
from tqdm import tqdm
import pickle
import aiohttp
import asyncio
import json


r1 = requests.get("https://dadosabertos.camara.leg.br/api/v2/deputados?idLegislatura=48&idLegislatura=49&idLegislatura=50&idLegislatura=51&idLegislatura=52&idLegislatura=53&idLegislatura=54&idLegislatura=55&idLegislatura=56&ordem=ASC&ordenarPor=nome&pagina=1&itens=1000")
r2 = requests.get("https://dadosabertos.camara.leg.br/api/v2/deputados?idLegislatura=48&idLegislatura=49&idLegislatura=50&idLegislatura=51&idLegislatura=52&idLegislatura=53&idLegislatura=54&idLegislatura=55&idLegislatura=56&ordem=ASC&ordenarPor=nome&pagina=2&itens=1000")
r3 = requests.get("https://dadosabertos.camara.leg.br/api/v2/deputados?idLegislatura=48&idLegislatura=49&idLegislatura=50&idLegislatura=51&idLegislatura=52&idLegislatura=53&idLegislatura=54&idLegislatura=55&idLegislatura=56&ordem=ASC&ordenarPor=nome&pagina=3&itens=1000")

lista_dados = r1.json()["dados"]+r2.json()["dados"]+r3.json()["dados"]
lista_ids = [x["id"] for x in lista_dados] 

legislaturas = range(48, 57)


if __name__ == '__main__':
	
	for id in tqdm(lista_ids):
		for legislatura in legislaturas:
			url = f"https://southamerica-east1-politic-topics.cloudfunctions.net/gerador-topicos?id_deputado={id}&id_legislatura={legislatura}"

			try:
				r = requests.get(url)
				j = r.json()
				pickle.dump(j, open(f'./topicos_discursos/{id}_{legislatura}.pkl', 'wb+'))

			except: 
				print(f'ERROR IN PROCESSING ID {id} LEGISLATURA {legislatura}')