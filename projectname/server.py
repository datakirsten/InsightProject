#import relevant tools to create a flask app
from flask import Flask, render_template, request
from projectname import getsynonyms
from flask_table import Table, Col

# Create the application object
app = Flask(__name__)

@app.route('/',methods=["GET","POST"]) #we are now using these methods to get user input
def home_page():
	return render_template('index.html')  # render a template

@app.route('/output')
def recommendation_output():
	#
	# Pull input
	some_input = request.args.get('user_input')

	# Case if input empty
	# Use the example from the website shown
	if some_input == "":
		some_input="https://towardsdatascience.com/how-discrimination-occurs-in-data-analytics-and-machine-learning-proxy-variables-7c22ff20792"

	###use the functions in the getsynonyms.py file to scrape the website text and provide the TextHelper tool output to the flask app
	some_title, some_maintext, someother_maintext = getsynonyms.getarticle(some_input)
	paragraph=[]
	word1=[]
	def1=[]
	keyword=[]
	parabefore=[]
	parakey=[]
	paraafter=[]
	items=[]
	class TableCls(Table):
		paragraphs = Col('Main Text')
		infrequent = Col('Defintiions')
	for paragraphs in some_maintext:
		paragraph.append(paragraphs)
		words=getsynonyms.getfrequencySUBTLEX(getsynonyms.spacy_nlp(str(paragraphs))[1])
		word1.append(words)
		def1.append(getsynonyms.getsynforinfreq(words))
		currentkeyword=getsynonyms.findkeywords(getsynonyms.spacy_nlp(str(paragraphs))[0])
		keyword.append(currentkeyword)
		currentdict={}
		currentdict['paragraphs']=paragraphs
		currentdict['infrequent']=words
		items.append(currentdict)
		if not currentkeyword:
			parabefore.append(paragraphs)
			parakey.append([])
			paraafter.append([])
		else:
			parapartition=paragraphs.partition(currentkeyword)
			parabefore.append(parapartition[0])
			parakey.append(parapartition[1])
			paraafter.append(parapartition[2])
	current_table=TableCls(items)
	##todo make the output more dynamic so it can adapt to number of paragraphs & generate the table accordingly
	return render_template("index.html",
		my_input=some_input,
		my_title=some_title,
		my_table=current_table,
		my_maintextbefore=parabefore[0],
		my_maintextkey=parakey[0],
		my_maintextafter=paraafter[0],
		my_first_word=word1[0],
		my_first_definition=def1[0],
		my_first_keyword=keyword[0],
		my_maintextbefore2=parabefore[1],
		my_maintextkey2=parakey[1],
		my_maintextafter2=paraafter[1],
		my_second_word=word1[1],
		my_second_definition=def1[1],
		my_second_keyword=keyword[1],
		my_maintextbefore3=parabefore[2],
		my_maintextkey3=parakey[2],
		my_maintextafter3=paraafter[2],
		my_third_word=word1[2],
		my_third_definition=def1[2],
		my_third_keyword=keyword[2],
		my_maintextbefore4=parabefore[3],
		my_maintextkey4=parakey[3],
		my_maintextafter4=paraafter[3],
		my_fourth_word=word1[3],
		my_fourth_definition=def1[3],
		my_fourth_keyword=keyword[3],
		my_maintextbefore5=parabefore[4],
		my_maintextkey5=parakey[4],
		my_maintextafter5=paraafter[4],
		my_fifth_word=word1[4],
		my_fifth_definition=def1[4],
		my_fifth_keyword=keyword[4],
		my_maintextbefore6=parabefore[5],
		my_maintextkey6=parakey[5],
		my_maintextafter6=paraafter[5],
		my_sixth_word=word1[5],
		my_sixth_definition=def1[5],
		my_sixth_keyword=keyword[5],
		my_maintextbefore7=parabefore[6],
		my_maintextkey7=parakey[6],
		my_maintextafter7=paraafter[6],
		my_seventh_word=word1[6],
		my_seventh_definition=def1[6],
		my_seventh_keyword=keyword[6],
		my_form_result="NotEmpty")


# start the server with the 'run()' method
if __name__ == "__main__":
	app.run(port=8000)  # will run locally http://127.0.0.1:5000/

