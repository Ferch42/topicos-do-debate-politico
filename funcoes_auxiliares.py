import re
import nltk
from nltk import word_tokenize
import string

regex_list = [r"(Orientação|Encaminhamento|Discussão|Emissão|Pedido|Questão de ordem|Esclarecimento|Declaração).*?(sobre|acerca|respeito|para|referente)",\
r"(nº|n°)(s)? \d+\.?\d*",r"alteração da(s)? Lei(s)?", r"de \d+", r"(relativa|relativo) (à|ao|aos)", \
r"Apelo.*?(por|pelo|pela|a respeito|sobre|acerca|de)", r"art\. \d+º?\.?\d*", \
r"\d+\.?\d*(º|ª)?", r"arts\.", r"§", r"R$", r"%", r"Apresentação.*?(de|da|do) ",\
r"votação em separado", r"Projeto de Lei", r"Medida Provisória", r"supressão", r"acerca", r"Decreto-Lei",\
r"revogação", r"Lei", r"dispositivo", r"destaques", r'destaque', r"ressalvado(s)?", r"ressalvada(s)?",\
r"inciso(s)?", r"redação", r'dada']

stop_words = nltk.corpus.stopwords.words('portuguese') + \
[punctuation for punctuation in string.punctuation] + \
["nºs", "nº", "§", "º", "i", 'ii', 'iii', "-a"] + \
["sobre", "lei", "art.", "projeto", "votação", "emenda", "proposta", "requerimento"] + \
["comissão", "decreto", "leis", "projetos", "emendas"] + \
["votações", "comissões", "orientação", "bancada", "mista", "orador"] + \
["medida", "provisória", "medidas", "provisórias", "questão", "ordem"] + \
["pauta", "pautas", "leitura", "discurso", "discussão"] + \
["plenário", "pedido", "destaque", "separado", "artigo"]+ \
["anúncio", "solicitações", "solicitação", "arts.", "inciso", "incisos"] + \
["caput", 'substitutivo', 'supressão', "assinaturas"] + \
["emissão", "parecer", "apresentação", "acerca", "apresentada"] + \
["apresentado", "submissão", 'transcurso'] + \
["alínea", "posicionamento", "regulamentação", "importância"]+ \
["declaração", "debate", "oradora","orador", "durante"] + \
['conversão', 'xii', 'constante', 'oferecido', 'oferecida', 'proposto'] + \
['discursos', 'referente', 'art', 'complementar', 'pec'] 


def preprocessa_sumario(texto):

	if not texto:
		return []
		
	discurso_preprocessado = texto
	# Remove as expressões regulares
	for r in regex_list:
		discurso_preprocessado = re.sub(r, "", discurso_preprocessado) 

	# Tokeniza e remove as stopwords
	return [w for w in word_tokenize(discurso_preprocessado.lower()) if w not in stop_words]



def processa_string_topico(t):

	palavras = t.replace(' ', '').replace('"','').split('+')
	palavras_separadas = [x.split('*') for x in palavras]
	soma_total_pesos = sum([float(x[0]) for x in palavras_separadas])

	return [{"text": x[1], "value": float(x[0])/soma_total_pesos*100} for x in palavras_separadas]