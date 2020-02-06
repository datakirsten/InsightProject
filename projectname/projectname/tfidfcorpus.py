import pandas as pd
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

import nltk
nltk.download('punkt')
nltk.download('stopwords')
import string
import spacy
#next step commented step is only necessary when loading of the english language library fails due to weird behaviour of anaconda
#from spacy.cli import download
#download('en')
nlp = spacy.load('en_core_web_sm')

df = pd.read_csv('/Users/Kirsten/InsightProjectLocalStuff/Ideas/MVP/Medium_AggregatedData.csv')#, sep='\t')
#print(df.columns)
#print(df.shape)
df.drop_duplicates(subset="text", inplace=True)
#print(df.shape)

currenttext=[]
for text in df['text']:
    currenttext.append(text)

def spacy_nlp(input_paragraph, allowed_postags=None):
    if allowed_postags is None:
        allowed_postags = ['NOUN', 'ADJ', 'VERB', 'ADV']
        #allowed_postags = ['NOUN']
    article_lemma = nlp(input_paragraph)
    texts_out = []
    for token in article_lemma:
        if token.pos_ in allowed_postags:
            texts_out.append(token)
    return texts_out,article_lemma
def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent))
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out


#####change this to make sure it takes the whole set of documents, not just the second
data_lemmatized = lemmatization(currenttext[1], allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])

print(data_lemmatized)


# Create Dictionary
id2word = corpora.Dictionary(data_lemmatized)

# Create Corpus
texts = data_lemmatized

# Term Document Frequency
corpus = [id2word.doc2bow(text) for text in texts]

# View
#print(corpus[:1])


# remove common words and tokenize
#stoplist = set('for a of the and to in'.split())
#texts = [
#    [word for word in document.lower().split() if word not in stoplist]
#    for document in corpus
#]

corpus_tok  = [tokenize(text) for text in corpus]
#print(corpus_tok[1])
lexicon = gensim.corpora.Dictionary(texts)
corpus_tok = [lexicon.doc2bow(text) for text in texts]
tfidf = gensim.models.TfidfModel(corpus_tok)
#tfidf   = gensim.models.TfidfModel(dictionary=lexicon, normalize=True)
vectors = [tfidf[lexicon.doc2bow(doc)] for doc in corpus]

lexicon.save_as_text('lexicon_pos.txt', sort_by_word=True)
tfidf.save('tfidf_pos.pkl')

#lexicon = gensim.corpora.Dictionary.load_from_text('lexicon.txt')
#tfidf = gensim.models.TfidfModel.load('tfidf.pkl')