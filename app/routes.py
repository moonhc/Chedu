from flask import render_template, request, url_for, redirect
from flask_socketio import send
from app import app, socketio

@app.route('/')
def index():
    #tmpDict = {}
    #tmpDict['userName'] = 'MoonHC'
    return render_template('Login.html')#, **tmpDict)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('chat', passcode=request.form['passcode'], uname=request.form['email']))
    else:
        return error_handling()

@app.route('/files', methods=['GET', 'POST'])

@app.route('/chat/<passcode>')
def chat(passcode, uname=None):
    if passcode == None :
        return error_handling()
    return render_template('chedu.html', passcode=passcode, uname=uname,
                                file_url="www.cs.uu.nl/docs/vakken/an/an-stablemarriage.ppt", 
                                filename="TEST", filedate="2017-00-00")

@app.route('/about')
def show_about():
    return render_template('about.html')

# guest_cnt = 0
@socketio.on('message')
def message_handler(msg):
    # if msg == 'new user':
    #     global guest_cnt
    #     guest_cnt += 1
    send(msg, broadcast=True)

def error_handling():
    return "Not vaild access!"
