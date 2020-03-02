# Import relevant tools for NLP and load the english language library
import spacy
# next commented step is only necessary when loading of the english language library fails due to weird behaviour of anaconda
# from spacy.cli import download
# download('en')
nlp = spacy.load('en_core_web_sm')
import pandas as pd
#import nltk
#nltk.download('wordnet')
import gensim
from gensim.summarization import keywords
import gensim.models as models
# Import the relevant tools to get text from a website
from bs4 import BeautifulSoup
import requests

# Example of an url input website
url = "https://towardsdatascience.com/chasing-the-data-coronavirus-802d8a1c4e9a" #"https://towardsdatascience.com/how-discrimination-occurs-in-data-analytics-and-machine-learning-proxy-variables-7c22ff20792"

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
    ###combine list elements if paragraphs is very short
    newparagraphtext=[]
    i=-1
    for text in paragraphtext:
        if len(text.split())<70 and newparagraphtext!=[] and len(newparagraphtext[i].split())<100:
            newparagraphtext[i]=newparagraphtext[i]+" "+text
        else:
            newparagraphtext.append(text)
            i=i+1


    return title, paragraphtext,newparagraphtext

##do preprocessing in spacy to get parts of of speech (POS) and lemmatized words
##return both the whole spacy preprocessing ouput (article_lemma) & a list of lemmas limited to POS=Noun
def spacy_nlp(input_paragraph, allowed_postags=None):
    if allowed_postags is None:
        allowed_postags = ['NOUN', 'ADJ', 'VERB', 'ADV']
        #allowed_postags = ['NOUN', 'VERB']
    article_lemma = nlp(input_paragraph)
    texts_out = []
    texts_out_lemma =[]
    for token in article_lemma:
        if token.pos_ in allowed_postags:
            texts_out.append(token)
            texts_out_lemma.append(token.lemma_)
    return texts_out,article_lemma,texts_out_lemma



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


###use gensim's text summarization to find keywords in a paragraph, returns the keyword
def findkeywords(input_paragraph):
    #at the moment POS=NOUN, because of earlier filtering in spacy_nlp
    noun_postags = ['NOUN']
    noun_chunk=[]
    input_text=' '.join(word.lemma_ for word in input_paragraph if word.pos_ in noun_postags)
    keyword = keywords(input_text, words=1, scores=False, lemmatize=False)
    for chunk in input_paragraph.noun_chunks:
        if keyword==chunk.root.text:
                noun_chunk=chunk
    return keyword, noun_chunk


###get infrequent words using TDIDF
def getfrequencyTFIDF(input_paragraph, bow=None):
    texts_out=[]
    texts_out_lemma = []
    allowed_postags = ['NOUN', 'ADJ', 'VERB', 'ADV']
    for token in input_paragraph:
        if token.pos_ in allowed_postags:
            texts_out.append(token)
            texts_out_lemma.append(token.lemma_)
    tfidf = models.TfidfModel.load('/Users/Kirsten/Documents/GitHub/InsightProject/projectname/projectname/tfidf_datascience20000.pkl')
    lexicon=gensim.corpora.Dictionary.load_from_text('/Users/Kirsten/Documents/GitHub/InsightProject/projectname/projectname/lexicon_datascience20000.txt')
    #tfidf = models.TfidfModel.load('/home/ubuntu/application/projectname/tfidf_datascience20000.pkl')
    #lexicon=gensim.corpora.Dictionary.load_from_text('/home/ubuntu/application/projectname/lexicon_datascience20000.txt')
    bow=lexicon.doc2bow(texts_out_lemma)
    corpus_tfidf = tfidf[bow]
    n_terms = 1
    top_terms = []
    for obj in sorted(corpus_tfidf, key=lambda x: x[1], reverse=True)[:n_terms]:
        top_terms=lexicon[obj[0]]
    b=texts_out_lemma.index(top_terms)
    x=texts_out[b]
    return top_terms,x





###get definitions (and synonyms,currently commented) using wordnet
def getsynforinfreq(word):
    from nltk.corpus import wordnet as wn  # Import wordnet from the NLTK
    syn = []
    definition=[]
    currentpos_name=word.pos_
    if currentpos_name=="ADV":
        currentpos_name="r"
    x=currentpos_name[0].lower()
    synsets=wn.synsets(str(word),pos=str(x))#,pos=currentpos)
    mysyn=[]
    for syn in synsets:
        definition.append(syn.definition())
        for lemma in syn.lemmas():
            if str(lemma.name()) != word.lemma_:
                mysyn.append(lemma.name())
    if definition==[]:
        definition.append("no definition found")
    if mysyn==[]:
        mysyn.append("no synonym found")
    return definition[0], mysyn[0]

