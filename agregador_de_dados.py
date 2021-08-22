import requests
from tqdm import tqdm
import json

# funções auxiliares

def seleciona_link(links, chave):

	link = [l for l in links if l['rel'] == chave]

	if link:
		return link[0]['href']

	else:
		return None

def captura_discursos(deputado):

	# captura todos os discursos do deputado
	requisicao_inicial = requests.get(
		f"https://dadosabertos.camara.leg.br/api/v2/deputados/{deputado['id']}/discursos",
		params = {'idLegislatura': deputado['idLegislatura']}
	)
	dados_requisicao = json.loads(requisicao_inicial.text)

	# link atual
	link_atual = seleciona_link(dados_requisicao['links'], 'self')

	# proximo link 
	proximo_link = seleciona_link(dados_requisicao['links'], 'next')

	# pega o link da ultima pagina
	link_final = seleciona_link(dados_requisicao['links'], 'last')

	# função auxiliar para adicionar o nome do deputado aos dicursos
	adiciona_nome_deputado = lambda disc: dict({'nomeDeputado': deputado['nome']}, **disc)
	
	discursos = [adiciona_nome_deputado(disc) for disc in dados_requisicao['dados']]
	
	while(link_atual!= link_final):
		# Itera pelas outras páginas
		if not proximo_link:
			break

		proxima_requisicao = requests.get(proximo_link)
		link_atual = proximo_link

		dados_requisicao = json.loads(proxima_requisicao.text)
		discursos += [adiciona_nome_deputado(disc) for disc in dados_requisicao['dados']]

		proximo_link = seleciona_link(dados_requisicao['links'], 'next')

	# Salva em disco os discursos
	with open(f"./discursos/{deputado['nome'].replace(' ', '_')}.txt", 'wt') as out:
   		out.write(json.dumps(discursos, indent=4, sort_keys=True))


	return discursos


def main():

	# Faz a requisição dos deputados
	requisicao_deputados = requests.get("https://dadosabertos.camara.leg.br/api/v2/deputados")
	dados_deputados = json.loads(requisicao_deputados.text)

	deputados = dados_deputados['dados']
	# por padrão todos os deputados estão na mesma Legislatura
	id_legislatura = dados_deputados['dados'][0]['idLegislatura']

	discursos = []
	for deputado in tqdm(deputados):

		discursos += captura_discursos(deputado)

	for discurso in discursos:

		print(discurso)



if __name__ == '__main__':
	main()