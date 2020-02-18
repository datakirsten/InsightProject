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

# next step commented step is only necessary when loading of the english language library fails due to weird behaviour of anaconda
# from spacy.cli import download
# download('en')
nlp = spacy.load('en_core_web_sm')

df = pd.read_csv('/Users/Kirsten/InsightProjectLocalStuff/Ideas/MVP/Medium_AggregatedData.csv')  # , sep='\t')
print(df.columns)
print(df.shape)
df.drop_duplicates(subset="text", inplace=True)
print(df.shape)
df.drop(df[df['language']!='en'].index, inplace=True)
print(df.shape)

currenttext = []
for text in df['text']:
    currenttext.append(text)

#print(currenttext[0:4])

xxx=currenttext[0:40000]

allowed_postags = ['NOUN', 'ADJ', 'VERB', 'ADV']
lemmatizedcorpus=[]
for text in xxx:
    article_lemma=nlp(text)
    texts_out=[]
    for token in article_lemma:
        if token.pos_ in allowed_postags:
            texts_out.append(token.lemma_)
    lemmatizedcorpus.append(texts_out)

#####change this to make sure it takes the whole set of documents, not just the second
#data_lemmatized = lemmatization(currenttext, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])


# Create Dictionary
datascience_dictionary = corpora.Dictionary(lemmatizedcorpus)

bow = []
for t in lemmatizedcorpus:
    bow.append(datascience_dictionary.doc2bow(t))

#bow

# Term Document Frequency
#corpus = [id2word.doc2bow(text) for text in texts]

# View
# print(corpus[:1])


# remove common words and tokenize
# stoplist = set('for a of the and to in'.split())
# texts = [
#    [word for word in document.lower().split() if word not in stoplist]
#    for document in corpus
# ]

#corpus_tok = [tokenize(text) for text in corpus]
# print(corpus_tok[1])
#lexicon = gensim.corpora.Dictionary(texts)
#corpus_tok = [lexicon.doc2bow(text) for text in texts]
tfidf = gensim.models.TfidfModel(bow)
# tfidf   = gensim.models.TfidfModel(dictionary=lexicon, normalize=True)
# vectors = [tfidf[lexicon.doc2bow(doc)] for doc in corpus]

datascience_dictionary.save_as_text('lexicon_datascience40000.txt', sort_by_word=True)
tfidf.save('tfidf_datascience40000.pkl')
datascience_dictionary.save('lexiconpkl40000.pkl')


#tf_obj = tfidf[bow[1]]
#sorted(tf_obj, key=lambda x: x[1], reverse=True)[:5]

#n_terms = 5

#top_terms = []
#for obj in sorted(tf_obj, key=lambda x: x[1], reverse=True)[:n_terms]:
 #   top_terms.append("{0:s} ({1:01.03f})".format(datascience_dictionary[obj[0]], obj[1]))

#print(top_terms)
# lexicon = gensim.corpora.Dictionary.load_from_text('lexicon.txt')
# tfidf = gensim.models.TfidfModel.load('tfidf.pkl')
