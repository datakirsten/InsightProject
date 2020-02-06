# Import relevant tools for NLP and load the english language library
import spacy
# next commented step is only necessary when loading of the english language library fails due to weird behaviour of anaconda
# from spacy.cli import download
# download('en')
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
import pandas as pd
import nltk
nltk.download('wordnet')
from gensim.summarization import keywords

# Import the relevant tools to get text from a website
from bs4 import BeautifulSoup
import requests

# Example of an url input website
url = "https://towardsdatascience.com/introduction-to-streaming-algorithms-b71808de6d29"

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
    newparagraphtext=[]
    previoustext = ""
    for paragraph in articlebody[:]:
         # get the text only
        text = paragraph.get_text()
        paragraphtext.append(text)
         ###something is still going wrong here...
        if len(text.split())<50:
            ####add if loop: if newparagraphtext=[] append to newparaghtext anyways, only if there is already an element add to prevoiustext
            if newparagraphtext==[]:
                newparagraphtext.append(text)
            else:
                previoustext=previoustext + " " + text
        else:
            mytext=previoustext + " " + text
            newparagraphtext.append(mytext)
            if len(mytext.split())>=50:
                previoustext=""
    return title, paragraphtext,newparagraphtext

b=getarticle(url)

##do preprocessing in spacy to get parts of of speech (POS) and lemmatized words
##return both the whole spacy preprocessing ouput (article_lemma) & a list of lemmas limited to POS=Noun
def spacy_nlp(input_paragraph, allowed_postags=None):
    if allowed_postags is None:
        #allowed_postags = ['NOUN', 'ADJ', 'VERB', 'ADV']
        allowed_postags = ['NOUN']
    article_lemma = nlp(input_paragraph)
    texts_out = []
    for token in article_lemma:
        if token.pos_ in allowed_postags:
            texts_out.append(token)
    return texts_out,article_lemma

c=spacy_nlp(str(b[1]))
#print(c[0])
#print(c[1])

###function that reads in the SUBTLEXus corpus and finds frequency of all input tokens in it
###returns the most infrequent word
def getfrequencySUBTLEX(input_paragraph):
    # read in subtlexus corpus, large corpus with frequency information
    corpus = pd.read_csv('/Users/Kirsten/Documents/GitHub/InsightProject/data/corpora/SUBTLEXusExcel2007.tsv', sep='\t', index_col="Word")
    #corpus = pd.read_csv('/home/ubuntu/application/data/corpora/SUBTLEXusExcel2007.tsv', sep='\t', index_col="Word")

    corpus.head()
    # for those word types carrying meaning (filter on POS), make a ranking according to frequency
    listofwordtypes = ['VERB', 'ADV', 'NOUN', 'ADJ']
    counter = 0
    corpus_results = []
    corpus_results_counter = []
    for token in input_paragraph:
        #filter based on POS, and check that word is actually in the corpus
        if (token.pos_ in listofwordtypes):
            try:
                corpus_results.append(corpus.loc[token.lemma_, 'Lg10WF'])
                corpus_results_counter.append(counter)
            except KeyError:
                pass
        counter = counter + 1
    outputtuple = sorted(zip(corpus_results, corpus_results_counter))[:2]
    mostinfrequent = input_paragraph[outputtuple[0][1]]
    return mostinfrequent

d=getfrequencySUBTLEX(c[1])
print(d)
###use gensim's text summarization to find keywords in a paragraph, returns the keyword
def findkeywords(input_paragraph):
    #at the moment POS=NOUN, because of earlier filtering in spacy_nlp
    input_text=' '.join(word.lemma_ for word in input_paragraph)
    keyword = keywords(input_text, words=1, scores=False, lemmatize=False)
    return keyword
e=findkeywords(c[0])
print(e)

###get infrequent words using TDIDF (still needs to be moved here from jupyter notebook)
def getfrequencyTFIDF(input_paragraph):
    lexicon = gensim.corpora.Dictionary.load_from_text('lexicon.txt')
    tfidf = gensim.models.TfidfModel.load('tfidf.pkl')
    corpus_tfidf = tfidf[input_paragraph]
    ###add a part that sorts based on frequency
    return corpus_tfidf


###get definitions (and synonyms,currently commented) using wordnet
def getsynforinfreq(word):
    from nltk.corpus import wordnet as wn  # Import wordnet from the NLTK
    syn = []
    currentpos="wn."+ word.pos_
    ###check whether it puts out the first or last synonym definition
    for synset in wn.synsets(str(word)):#,pos=str(currentpos)):
        ##get the synonyms
        # for lemma in synset.lemmas():
        # if str(lemma.name()) != word:
        #   syn.append(lemma.name())  # add the synonyms
        return synset.definition() #, currentpos

