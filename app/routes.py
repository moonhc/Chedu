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
        return 'Not valid access'

@app.route('/chat/<passcode>')
@app.route('/chat/<passcode>/<uname>')
def chat(passcode, uname=None):
    return render_template('chedu.html', passcode=passcode, uname=uname)

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
