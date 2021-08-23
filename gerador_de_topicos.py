from datetime import datetime
from dateutil.relativedelta import relativedelta
from gensim import corpora
from sklearn.manifold import TSNE
import gensim
from google.cloud import firestore
from tqdm import tqdm
from funcoes_auxiliares import processa_string_topico

NUMERO_DE_TOPICOS = 20

def main():

	# Começo da lesgislatura atual
	data_de_inicio = datetime(2019,2,1)
	db = firestore.Client()

	while(data_de_inicio< datetime.now()):

		print(f"Processando : {data_de_inicio}")
		discursos_do_mes = db.collection('discursos').where("dataHoraDiscurso", ">=", data_de_inicio).where('dataHoraDiscurso', '<=', data_de_inicio +  relativedelta(months=+1)).get()

		if not discursos_do_mes:
			data_de_inicio = data_de_inicio +  relativedelta(months=+1)
			continue

		sumarios_tokenizados = [x.to_dict()['sumarioPreProcessado'] for x in discursos_do_mes]
		dicionario = corpora.Dictionary(sumarios_tokenizados)

		sumarios_vetorizados = [dicionario.doc2bow(s) for s in tqdm(sumarios_tokenizados)]

		modelo_lda = ldamodel = gensim.models.ldamodel.LdaModel(sumarios_vetorizados, num_topics = NUMERO_DE_TOPICOS, id2word=dicionario, passes=10, alpha = 'auto', eta = 'auto')

		tsne_topicos = TSNE(n_components=2).fit_transform(modelo_lda.get_topics())

		topicos = modelo_lda.print_topics(num_words=20)
		db.collection('topicos').add({
				"dataInicio": data_de_inicio,
				"dataFim": data_de_inicio +  relativedelta(months=+1),
				"topicos": [{'palavras' : processa_string_topico(t[1]) , 'tsneCoords' : tsne_topicos[t[0]].tolist(), 'idTopico': t[0]} for t in topicos]
			})

		data_de_inicio = data_de_inicio +  relativedelta(months=+1)


if __name__ == '__main__':
	main()

