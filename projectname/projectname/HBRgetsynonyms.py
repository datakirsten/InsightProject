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
# Location of website and getting the content with BeautifulSoup
url = "https://hbr.org/2018/11/ego-is-the-enemy-of-good-leadership"


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
    # articlebody = soup.find(class_='article article-first-row').find_all('p')
    articlebody = soup.find(class_='content-area--article column').find_all('p')

    # put main body of text into a list with the text structured paragraph by paragraph
    for paragraph in articlebody[:]:
        # get the text only
        text = paragraph.get_text()
        paragraphtext.append(text)

    return title,paragraphtext
    #print(title)
    # print(articlebody)
    #print(paragraphtext[0])

#mytitle,mycurrentparagraph=getarticle(url)
#print(mytitle)
#print(mycurrentparagraph[0])

#def lemmatize(input_article):
  #  article_lemma= nlp(input_article)
 #   return article_lemma

#para_lemma=lemmatize(mycurrentparagraph[0])

def findkeywords(input_paragraph):
    keyword=keywords(input_paragraph, words=1,scores=True, lemmatize=True,pos_filter=('NN', 'VB'))
    return keyword

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
    secondmostinfrequent=article_lemma[outputtuple[1][1]]
    return(mostinfrequent, secondmostinfrequent)
   # return outputtuple


#currentmostinfrequent,currentsecondmostinfrequent=getfrequencySUBTLEX(mycurrentparagraph[0])
#print(currentmostinfrequent,currentsecondmostinfrequent)

####fix this!!!
def getsynforinfreq(word):
    from nltk.corpus import wordnet as wn  # Import wordnet from the NLTK
    syn = []
    for synset in wn.synsets(str(word)):
        #for lemma in synset.lemmas():
            #if str(lemma.name()) != word:
             #   syn.append(lemma.name())  # add the synonyms
        return(synset.definition())

#currentdefinition1=getsynforinfreq(getfrequencySUBTLEX(mycurrentparagraph[0])[0])

#currentdefinition2=getsynforinfreq(getfrequencySUBTLEX(mycurrentparagraph[0])[1])
#print(currentdefinition1,currentdefinition2)
