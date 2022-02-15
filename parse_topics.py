import requests
import re
from sklearn.feature_extraction.text import TfidfVectorizer


r = requests.get("https://southamerica-east1-politic-topics.cloudfunctions.net/gerador-topicos?id_deputado=204534&id_legislatura=56")

def preprocess_token(token):

	return re.sub('\d', '' ,token.replace('/', '')).strip()

def identity_tokenizer(text):
    return text

data = [[preprocess_token(token) for token in d] for d in r.json()]
tfidf = TfidfVectorizer(tokenizer=identity_tokenizer, stop_words='portuguese', lowercase=False)    
transformed_data = tfidf.fit_transform(data)

feature_names = tfidf.get_feature_names()