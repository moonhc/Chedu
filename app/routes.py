from flask import render_template
from app import app

@app.route('/')
def index():
    tmpDict = {}
    tmpDict['userName'] = 'MoonHC'
    return render_template('index.html', **tmpDict)

@app.route('/chat')
def chat():
    return render_template('chedu.html')
