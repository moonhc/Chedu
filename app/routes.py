from flask import render_template
from flask_socketio import send
from app import app, socketio

@app.route('/')
def index():
    tmpDict = {}
    tmpDict['userName'] = 'MoonHC'
    return render_template('index.html', **tmpDict)

@app.route('/chat')
def chat():
    return render_template('chedu.html')

# guest_cnt = 0
@socketio.on('message')
def message_handler(msg):
    # if msg == 'new user':
    #     global guest_cnt
    #     guest_cnt += 1
    send(msg, broadcast=True)
