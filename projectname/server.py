#import relevant tools to create a flask app
from flask import Flask, render_template, request
from projectname import getsynonyms
#from flask_wtf import FlaskForm
#from wtforms import BooleanField
#from flask_table import Table, Col

# Create the application object
app = Flask(__name__)

@app.route('/',methods=["GET","POST"]) #we are now using these methods to get user input
def home_page():
	return render_template('index.html')  # render a template

@app.route('/output')
def recommendation_output():
	# Pull input
	some_input = request.args.get('user_input')
	radio_value=request.args.get('syndef')
	#assert radio_value == 5, f"Radio Value {radio_value}"
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
	for paragraphs in some_maintext:
		paragraph.append(paragraphs)
		words=getsynonyms.getfrequencySUBTLEX(getsynonyms.spacy_nlp(str(paragraphs))[1])
		word1.append(words)
		if radio_value=="1":
			def1.append(getsynonyms.getsynforinfreq(words)[0])
			whichdeforsyn="Synonyms"
		else:
			def1.append(getsynonyms.getsynforinfreq(words)[1])
			whichdeforsyn = "Definitions"
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
	for i in range(0,20):
		parabefore.append("")
		parakey.append("")
		paraafter.append("")
		def1.append("")
		keyword.append("")
		word1.append("")
	##todo make the output more dynamic so it can adapt to number of paragraphs & generate the table accordingly
	return render_template("index.html",
		#my_input=some_input,
		my_radiovalue=radio_value,
		my_title=some_title,
		parabefore=parabefore,
		parakey=parakey,
		paraafter=paraafter,
		def1=def1,
		which_output=whichdeforsyn,
		keyword=keyword,
		word1=word1,
		my_form_result="NotEmpty")


# start the server with the 'run()' method
if __name__ == "__main__":
	app.run(port=8000)  # will run locally http://127.0.0.1:5000/

