# Import relevant tools for NLP and load the english language library
import spacy
#from spacy.cli import download
#download('en')
nlp = spacy.load('en_core_web_sm')
#import numpy as np
import pandas as pd

import nltk
nltk.download('wordnet')
# Import the relevant tools to get text from a website
from bs4 import BeautifulSoup
import requests
from gensim.summarization import keywords

#def findkeywords(input_paragraph):

text = '''When I decided I wanted to become a data scientist, the first thing I wanted to learn was how to write computer code. Since I had never coded before it was a complete unknown. I figured that if I really hated writing code, then data science would not be a great fit for me. So it seemed like a good place to start.'''
a=keywords(text, words=1,scores=False, lemmatize=True)



parapartition=text.partition(a)

print(parapartition[0])