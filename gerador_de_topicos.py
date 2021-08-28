from datetime import datetime
from gensim import corpora
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
import gensim
from google.cloud import firestore
from mockfirestore import MockFirestore
import pickle
from tqdm import tqdm
from funcoes_auxiliares import processa_string_topico, calcula_probabilidade_to_topico_media

NUMERO_DE_TOPICOS = 32
NUMERO_DE_AGRUPAMENTOS = 7
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

			matrix_de_topicos = modelo_lda.get_topics()
			tsne_topicos = TSNE(n_components=2).fit_transform(matrix_de_topicos)

			agrupamentos_de_topicos = KMeans(n_clusters=NUMERO_DE_AGRUPAMENTOS).fit_predict(tsne_topicos).tolist()
			#print(agrupamentos_de_topicos)
			topicos = modelo_lda.print_topics(num_topics=-1, num_words=20)

			distribuicao_topicos = modelo_lda.get_document_topics(sumarios_vetorizados)

			distribuicao_media_topicos = calcula_probabilidade_to_topico_media(distribuicao_topicos, NUMERO_DE_TOPICOS)
			
			topico_dict = {
					"dataInicio": data_de_inicio,
					"dataFim": data_fim,
					"topicos": [{'palavras' : processa_string_topico(t[1]) , 
					'tsneCoords' : tsne_topicos[t[0]].tolist(),
					'distribuicaoMedia': distribuicao_media_topicos[t[0]],
					'idTopico': t[0], 
					'grupoTopico': agrupamentos_de_topicos[t[0]]} for t in topicos]
			}
			#print(topico_dict)
			db_real.collection('topicos').add(topico_dict)
			data_fim = adiciona_mes(data_fim)

		data_de_inicio = adiciona_mes(data_de_inicio)


if __name__ == '__main__':
	main()

