import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from tqdm import tqdm
import re
from pprint import pprint

def preprocess_token(token):

	return re.sub('\d', '' ,token.replace('/', '')).strip()

def identity_tokenizer(text):
	return text

def main():

	all_topics = [] # corpus
	for file in tqdm(os.listdir('topicos_discursos')):

		with open(f'topicos_discursos/{file}', "rb") as f:
			data = pickle.load(f)

		all_topics += data

	all_topics_preprocessed = [[preprocess_token(token) for token in d] for d in tqdm(all_topics)]
	tfidf = TfidfVectorizer(tokenizer=identity_tokenizer, lowercase=False) 
	tfidf.fit(all_topics_preprocessed)

	feature_names = tfidf.get_feature_names()
	idf = tfidf.idf_

	with open('topicos_discursos/204534_56.pkl', 'rb') as f:
        tabata = pickle.load(f)

    tabata_preprocessada = [[preprocess_token(t) for t in d] for d in tabata]

    tfidf_tabata = tfidf.transform(tabata_preprocessada).toarray()

    primeiro_discurso_tabata = tfidf_tabata[0]
    tfidf_ordenado_tabata_primeiro_discurso = sorted(zip(feature_names, tfidf_tabata[0]), key = lambda x: x[1] , reverse = True)

    mapa_idf = {f:i for f,i in zip(feature_names, idf)}

if __name__ == '__main__':
	main()