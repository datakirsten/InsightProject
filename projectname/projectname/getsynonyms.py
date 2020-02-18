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
        # if len(text.split())<100:
        #     ####add if loop: if newparagraphtext=[] append to newparaghtext anyways, only if there is already an element add to prevoiustext
        #     if newparagraphtext==[]:
        #         newparagraphtext.append(text)
        #     else:
        #         previoustext=previoustext + " " + text
        # else:
        #     mytext=previoustext + " " + text
        #     newparagraphtext.append(mytext)
        #     if len(mytext.split())>=100:
        #         previoustext=""
    newparagraphtext=paragraphtext.copy()
    mylist = []
    x=len(paragraphtext[0].split())
    for i in range(len(paragraphtext)):
     #  len(paragraphtext[0].split())
        newparagraphtext[i-1:i]=[''.join(newparagraphtext[i-1:i])]
    return title, paragraphtext,newparagraphtext

b=getarticle(url)
#print(b[1])
#print(b[2])



##do preprocessing in spacy to get parts of of speech (POS) and lemmatized words
##return both the whole spacy preprocessing ouput (article_lemma) & a list of lemmas limited to POS=Noun
def spacy_nlp(input_paragraph, allowed_postags=None):
    if allowed_postags is None:
        #allowed_postags = ['NOUN', 'ADJ', 'VERB', 'ADV']
        allowed_postags = ['NOUN']
    article_lemma = nlp(input_paragraph)
    texts_out = []
    texts_out_lemma =[]
    for token in article_lemma:
        if token.pos_ in allowed_postags:
            texts_out.append(token)
            texts_out_lemma.append(token.lemma_)
    return texts_out,article_lemma,texts_out_lemma

c=spacy_nlp(str(b[1][12]))
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

#d=getfrequencySUBTLEX(c[1])
#print(d)
###use gensim's text summarization to find keywords in a paragraph, returns the keyword
def findkeywords(input_paragraph):
    #at the moment POS=NOUN, because of earlier filtering in spacy_nlp
    input_text=' '.join(word.lemma_ for word in input_paragraph)
    keyword = keywords(input_text, words=1, scores=False, lemmatize=False)
    return keyword
#e=findkeywords(c[0])
#print(e)
###get infrequent words using TDIDF (still needs to be moved here from jupyter notebook)
def getfrequencyTFIDF(input_paragraph, bow=None):
    texts_out=[]
    texts_out_lemma = []
    allowed_postags = ['NOUN', 'ADJ', 'VERB', 'ADV']
    for token in input_paragraph:
        if token.pos_ in allowed_postags:
            texts_out.append(token)
            texts_out_lemma.append(token.lemma_)
 #   input_text = ' '.join(word.lemma_ for word in input_paragraph)
 #   lexicon = corpora.Dictionary.load_from_text('lexicon.txt')
    tfidf = models.TfidfModel.load('/Users/Kirsten/Documents/GitHub/InsightProject/projectname/projectname/tfidf_datascience10000.pkl')
    lexicon=gensim.corpora.Dictionary.load_from_text('/Users/Kirsten/Documents/GitHub/InsightProject/projectname/projectname/lexicon_datascience10000.txt')
   # lexicon=load('lexicon_datascience.txt')
    #bow = []
    #for t in input_paragraph:
    bow=lexicon.doc2bow(texts_out_lemma)
    corpus_tfidf = tfidf[bow]
  #  tf_obj = tfidf[bow[1]]
    #sorted(corpus_tfidf, key=lambda x: x[1], reverse=True)[:5]
    n_terms = 1
    top_terms = []
    for obj in sorted(corpus_tfidf, key=lambda x: x[1], reverse=True)[:n_terms]:
        top_terms=lexicon[obj[0]]
        #top_terms.append("{0:s} ({1:01.03f})".format(lexicon[obj[0]], obj[1]))
   # print(top_terms)
    return top_terms

f=getfrequencyTFIDF(c[1])
print(f)

###get definitions (and synonyms,currently commented) using wordnet
def getsynforinfreq(word):
    from nltk.corpus import wordnet as wn  # Import wordnet from the NLTK
    syn = []
    definition=[]
    #currentpos_name=word.pos_
    #if currentpos_name=="ADV":
     #   currentpos_name="r"
    #x=currentpos_name[0].lower()
    synsets=wn.synsets(str(word))#,pos=str(x))#,pos=currentpos)
    #definition=synsets[0].definition()
    mysyn=[]
    #synonym=synsets[0].hypernyms()
    for syn in synsets:
        definition.append(syn.definition())
        for lemma in syn.lemmas():
            if str(lemma.name()) != word:#.lemma_:
                mysyn.append(lemma.name())
    if definition==[]:
        definition.append("no definition found")
    if mysyn==[]:
        mysyn.append("no synonym found")
    return definition[0], mysyn[0] #definition[0] #definition[0] #, mysyn[0]

g=getsynforinfreq(f)
print(g)


