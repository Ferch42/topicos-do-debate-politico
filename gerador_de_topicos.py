from datetime import datetime
from gensim import corpora
from sklearn.manifold import TSNE
import gensim
from google.cloud import firestore
from mockfirestore import MockFirestore
import pickle
from tqdm import tqdm
from funcoes_auxiliares import processa_string_topico

NUMERO_DE_TOPICOS = 20
datetime_format = "%Y-%m-%dT%H:%M"

def adiciona_mes(data):

	d = datetime.strptime(data, datetime_format)

	if d.month==12:

		return datetime(d.year+1, 1, d.day).strftime(datetime_format)

	else:
		return datetime(d.year, d.month+1, d.day).strftime(datetime_format)

def main():

	# Começo da lesgislatura atual
	data_de_inicio = "2019-01-01T00:00"
	
	# Utilize essa versão para utilizar o banco de dados online
	
	db_real = firestore.Client()
	# Fix para acesso local dos dados
	print('Utilizando a versão local')
	db = MockFirestore()

	with open('db.pkl', 'rb') as f:
		# Arquivo db é uma versão serializada do bd remoto
		db._data = pickle.load(f)

	while(data_de_inicio< datetime.now().strftime(datetime_format)):

		data_fim = adiciona_mes(data_de_inicio)

		while(data_fim< datetime.now().strftime(datetime_format)):
			
			print(f"Processando : {data_de_inicio} até {data_fim}")
			discursos_dos_meses = db.collection('discursos').where("dataHoraInicio", ">=", data_de_inicio).where('dataHoraInicio', '<=', data_fim).get()
			discursos_dos_meses = list(discursos_dos_meses)
			
			if not discursos_dos_meses:
				data_fim = adiciona_mes(data_fim)
				continue

			sumarios_tokenizados = [x.to_dict()['sumarioPreProcessado'] for x in discursos_dos_meses]
			dicionario = corpora.Dictionary(sumarios_tokenizados)

			sumarios_vetorizados = [dicionario.doc2bow(s) for s in tqdm(sumarios_tokenizados)]

			modelo_lda  = gensim.models.ldamodel.LdaModel(sumarios_vetorizados, num_topics = NUMERO_DE_TOPICOS, id2word=dicionario, passes=10, alpha = 'auto', eta = 'auto')

			tsne_topicos = TSNE(n_components=2).fit_transform(modelo_lda.get_topics())

			topicos = modelo_lda.print_topics(num_words=50)
			db_real.collection('topicos').add({
					"dataInicio": data_de_inicio,
					"dataFim": data_fim,
					"topicos": [{'palavras' : processa_string_topico(t[1]) , 'tsneCoords' : tsne_topicos[t[0]].tolist(), 'idTopico': t[0]} for t in topicos]
				})
			data_fim = adiciona_mes(data_fim)

		data_de_inicio = adiciona_mes(data_de_inicio)


if __name__ == '__main__':
	main()

