import pandas as pd
import sklearn as sk
import numpy as np
import math
#df = pd.read_csv('/Users/Kirsten/InsightProjectLocalStuff/Ideas/MVP/Medium_AggregatedData.csv')  # , sep='\t')
#df.drop_duplicates(subset="text", inplace=True)
#print(df.shape)
#df.drop(df[df['language']!='en'].index, inplace=True)
#print(df.shape)

mytext=[]
mytext.append('The car is driven on the road')
mytext.append('The truck is driven on the highway')
currenttext = []

#for text in df['text']:
for text in mytext:
    currenttext.append(text)


#print(currenttext[0:4])

#xxx=currenttext[0:20]

#TF=term i frequency in document object/ total words in objectI
#IDF=log2(no of total documents/documents with term i)

#TF={} per word in corpus per document count its frequency
#IDF={} in how many documents does the word occur
#TF-IDF={} per word per document what is the TF-IDF value
thedocuments=[]
for document in currenttext:
    thedocuments.append(document.split(" "))

dictofallwords=set().union(*thedocuments)

dictoftfs={}
i=0
###get TF
for document in thedocuments:
    dictoftfs[i]=dict.fromkeys(dictofallwords, 0)
    for word in document:
        dictoftfs[i][word]+=1
    i+=1

idf=dict.fromkeys(dictofallwords, 0)

idf2=dict.fromkeys(dictofallwords, 0)
N=len(thedocuments)
for document in thedocuments:
    for word in dictofallwords:
        if word in document:
            idf[word]+=1

for word in dictofallwords:
    idf2[word]=np.log10(2/idf[word])

##TF-IDF
tfidf={}
i=0
for document in thedocuments:
    tfidf[i]=dict.fromkeys(dictofallwords, 0)
    for word in document:
        tfidf[i][word]=dictoftfs[i][word]*idf2[word]
    i+=1


print(tfidf[0])
print(tfidf[1])
