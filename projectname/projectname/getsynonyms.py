# Import relevant tools for NLP and load the english language library
import spacy
#next step commented step is only necessary when loading of the english language library fails due to weird behaviour of anaconda
#from spacy.cli import download
#download('en')
nlp = spacy.load('en_core_web_sm')
#import numpy as np
import pandas as pd
import nltk
nltk.download('wordnet')
from gensim.summarization import keywords

#from sklearn.pipeline import Pipeline
#from sklearn.feature_extraction.text import TfidfVectorizer
# Import the relevant tools to get text from a website
from bs4 import BeautifulSoup
import requests

# Example of an url input website
##url = "https://towardsdatascience.com/can-analysts-and-statisticians-get-along-5c9a65c8d056"

###function to scrape text from a medium article
def getarticle(currenturl):
    webpage = requests.get(currenturl)
    content_page = webpage.content
    soup = BeautifulSoup(content_page, 'html.parser')
    title = []
    paragraphtext = []
    # get article title
    try:
        abody = soup.find('title')
        title = abody.get_text()
    except:
        title = 'Anonymous'
    ## get main article text
    articlebody = soup.find(class_='meteredContent').find_all('p')
    # put main body of text into a list with the text structured paragraph by paragraph
    for paragraph in articlebody[:]:
        # get the text only
        text = paragraph.get_text()
        paragraphtext.append(text)
    ###try to combine short paragraphs into one
   # newparagraphtext = [[paragraphtext[0]]]
   #  for paragraph in paragraphtext[1:]:
   #      if len(paragraph.split())<20:
   #          newparagraphtext[-1][0]=newparagraphtext[-1][0]+ paragraph
   #      else:
   #          newparagraphtext.append([paragraph])

    return title,paragraphtext #,newparagraphtext

###function that reads in the SUBTLEXus corpus and finds frequency of all input tokens in it
###returns the most infrequent word
def getfrequencySUBTLEX(input_paragraph):
    # read in subtlexus corpus, large corpus with frequency information
    article_lemma = nlp(input_paragraph)
    corpus = pd.read_csv('/Users/Kirsten/Documents/GitHub/InsightProject/data/corpora/SUBTLEXusExcel2007.tsv', sep='\t', index_col="Word")
    corpus.head()
    # for those word types carrying meaning, make a ranking according to frequency
    listofwordtypes = ['VERB', 'ADV', 'NOUN', 'ADJ']
    counter = 0
    corpus_results = []
    corpus_results_counter = []
    for token in article_lemma:
        if (token.pos_ in listofwordtypes):
            try:
                corpus_results.append(corpus.loc[token.lemma_, 'Lg10WF'])
                corpus_results_counter.append(counter)
            except KeyError:
                pass
        counter = counter + 1
    outputtuple = sorted(zip(corpus_results, corpus_results_counter))[:2]
    mostinfrequent=article_lemma[outputtuple[0][1]]
 #   secondmostinfrequent=article_lemma[outputtuple[1][1]]
    return(mostinfrequent)

#for paragraph in b[1]:
 #   a=getfrequencySUBTLEX(str(paragraph))
  #  print(a)

###use gensim's text summarization to find keywords in a paragraph, returns the keyword
###lemmatization part does not work right now!
def findkeywords(input_paragraph):
    keyword=keywords(input_paragraph, words=1,scores=False, lemmatize=True, pos_filter=('NN', 'NNS'))
    return keyword

###gensim's entropy based keyword finder
#def findkeywords_mz(input_paragraph):
#    keyword=keywords(input_paragraph, words=1,scores=False, lemmatize=False, pos_filter=('NN', 'NNS'))
#    return keyword

###get infrequent words using TDIDF (still needs to be moved here from jupyter notebook
#def getfrequencyTFIDF(input_paragraph):
 #   vectorizer = TfidfVectorizer()
 #   X_articles_tfidf = vectorizer.fit_transform(df[input_paragraph])  # remember to use the original X_train set
#    X_articles_tfidf.shape


###get definitions (and synonyms) using wordnet
def getsynforinfreq(word):
    from nltk.corpus import wordnet as wn  # Import wordnet from the NLTK
    syn = []
    for synset in wn.synsets(str(word)):
        ##get the synonyms
        #for lemma in synset.lemmas():
            #if str(lemma.name()) != word:
             #   syn.append(lemma.name())  # add the synonyms
        return(synset.definition())

