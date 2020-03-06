# Import relevant tools for NLP and load the english language library
import spacy
# next commented step is only necessary when loading of the english language library fails due to weird behaviour of anaconda
# from spacy.cli import download
# download('en')
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
import pandas as pd
import nltk
nltk.download('wordnet')
import gensim
from gensim.summarization import keywords
import gensim.corpora as corpora
import gensim.models as models

# Import the relevant tools to get text from a website
from bs4 import BeautifulSoup
import requests

# Example of an url input website
url = "https://towardsdatascience.com/chasing-the-data-coronavirus-802d8a1c4e9a" #"https://towardsdatascience.com/how-discrimination-occurs-in-data-analytics-and-machine-learning-proxy-variables-7c22ff20792"
tfidf = models.TfidfModel.load('/Users/Kirsten/Documents/GitHub/InsightProject/projectname/projectname/tfidf_datascience20000.pkl')
lexicon=gensim.corpora.Dictionary.load_from_text('/Users/Kirsten/Documents/GitHub/InsightProject/projectname/projectname/lexicon_datascience20000.txt')
corpus_tfidf = tfidf[bow]
lsi_model = models.LsiModel(corpus_tfidf, id2word=lexicon, num_topics=2)
corpus_lsi = lsi_model[corpus_tfidf]

#h=createtopics(g[2])
#h.print_topics(2)
##pyLDAvis.enable_notebook()
#vis=pyLDAvis.gensim.prepare(h,g[2],lexicon)
#vis