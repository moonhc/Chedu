from flask import render_template, request
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
        return 'POST'
    else:
        return 'GET'

@app.route('/chat/<passcode>')
@app.route('/chat/<passcode>/<uname>')
def chat(passcode, uname=None):
    return render_template('chedu.html', passcode=passcode)

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
