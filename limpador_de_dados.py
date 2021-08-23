from google.cloud import firestore
from funcoes_auxiliares import preprocessa_sumario
from tqdm import tqdm

def main():

	db = firestore.Client()

	discursos = db.collection('discursos').get()

	for disc in tqdm(discursos):

		# Adiciona sumario preprocessado ao banco de dados
		sumario = disc.to_dict()['sumario']
		disc.reference.update({"sumarioPreProcessado":preprocessa_sumario(sumario) })


if __name__ == '__main__':
	main()