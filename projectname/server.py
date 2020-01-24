from flask import Flask, render_template, request

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

	# Case if empty
	if some_input == "'":
		return render_template("index.html",
			my_input=some_input,
			my_form_result="Empty")
	else:
		some_title= "Ego Is the Enemy of Good Leadership"#title
		some_maintext = "On his first day as CEO of the Carlsberg Group, a global brewery and beverage company, Cees ‘t Hart was given a key card by his assistant. The card locked out all the other floors for the elevator so that he could go directly to his corner office on the 20th floor. And with its picture windows, his office offered a stunning view of Copenhagen. These were the perks of his new position, ones that spoke to his power and importance within the company."#paragraph
		first_synonym = "perks" #synonym1
		first_definition = "fringe benefits" #def1
		second_synonym = "inflated" #synonym2
		second_definition = "expand"#def2
		return render_template("index.html",
			my_input=some_input,
			my_title=some_title,
			my_maintext=some_maintext,
			my_first_synonym=first_synonym,
			my_first_definition=first_definition,
			my_second_synonym=second_synonym,
			my_second_definition=second_definition,
			my_form_result="NotEmpty")


# start the server with the 'run()' method
if __name__ == "__main__":
	app.run(debug=True)  # will run locally http://127.0.0.1:5000/

