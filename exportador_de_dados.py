import os
import json
from tqdm import tqdm
from google.cloud import firestore
from datetime import datetime


def main():

	db = firestore.Client()
	discursos = []
	for file in tqdm(os.listdir('./discursos')):

		with open(f'./discursos/{file}') as f:
			disc = json.load(f)
		discursos += disc

	for d in tqdm(discursos):

		# transforma data em datetime
		d.update({'dataHoraDiscurso': datetime.strptime(d['dataHoraInicio'], "%Y-%m-%dT%H:%M")})
		db.collection('discursos').add(d)


if __name__ == '__main__':
	main()