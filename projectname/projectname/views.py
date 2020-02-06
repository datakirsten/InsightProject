from flask import render_template
from flask import request 
from projectname import app

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
       title = 'Home', user = { 'nickname': 'K' },
       )
