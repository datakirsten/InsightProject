# TextHelper

TextHelper is an app that takes a text, for example a data science article on a medium website or a legal document, and aids the quick and successful reading comprehension of the text with NLP tools. This will help people who frequently have to scan texts for specific information. 

These tool are:
1. Providing synonyms and definitions for unfamiliar words
2. Providing headers for paragraphs to give context
3. Highlighting keywords

# Structure of the project
The important files are located in the folder projectname
index.html: front end of the html app
server.py: connection between front and back end
getsynonyms.py: 'backend', functions for scraping text + the different NLP tools
tfidcorpus.py: built data science related article corpus

# Conventions
Built with python 3.0, flask and html
requires the following packages and tools:
spacy
gensim
pandas
Beautiful Soup
requests

#you can look at the app that was built here:
http://understandingdata.xyz



