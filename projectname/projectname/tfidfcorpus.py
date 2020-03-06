import pandas as pd
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
import gensim.models as models
import pyLDAvis
import pyLDAvis.gensim
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

xxx=currenttext[0:20]

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

bow = [datascience_dictionary.doc2bow(text) for text in lemmatizedcorpus]
#bow = []
#for t in lemmatizedcorpus:
#    bow.append(datascience_dictionary.doc2bow(t))

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
corpus_tfidfm=tfidf[bow]

mylda=gensim.models.LdaModel(corpus_tfidfm,num_topics=30,id2word=datascience_dictionary)
#mylda=gensim.models.HdpModel(corpus_tfidfm,id2word=datascience_dictionary)
topics = mylda.print_topics(num_words=4)
for topic in topics:
    print(topic)

# Visualize the topics
#pyLDAvis.enable_notebook()
vis = pyLDAvis.gensim.prepare(mylda, corpus_tfidfm, datascience_dictionary)
pyLDAvis.save_html(vis, 'LDA_Visualization.html')
#models.LdaModel
#h=createtopics(g[2])
#h.print_topics(2)
##pyLDAvis.enable_notebook()
#vis=pyLDAvis.gensim.prepare(h,g[2],lexicon)
#vis


#lsi_model = gensim.models.LsiModel(corpus_tfidfm, id2word=datascience_dictionary, num_topics=2)  # initialize an LSI transformation
#corpus_lsi = lsi_model[corpus_tfidfm]  # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi

#lsi_model.print_topics(2)

#for doc, as_text in zip(corpus_lsi, lemmatizedcorpus):
 #   print(doc, as_text)
# tfidf   = gensim.models.TfidfModel(dictionary=lexicon, normalize=True)
# vectors = [tfidf[lexicon.doc2bow(doc)] for doc in corpus]

##datascience_dictionary.save_as_text('lexicon_datascience20000.txt', sort_by_word=True)
#tfidf.save('tfidf_datascience20000.pkl')
#datascience_dictionary.save('lexiconpkl20000.pkl')


#tf_obj = tfidf[bow[1]]
#sorted(tf_obj, key=lambda x: x[1], reverse=True)[:5]

#n_terms = 5

#top_terms = []
#for obj in sorted(tf_obj, key=lambda x: x[1], reverse=True)[:n_terms]:
 #   top_terms.append("{0:s} ({1:01.03f})".format(datascience_dictionary[obj[0]], obj[1]))

#print(top_terms)
# lexicon = gensim.corpora.Dictionary.load_from_text('lexicon.txt')
# tfidf = gensim.models.TfidfModel.load('tfidf.pkl')
