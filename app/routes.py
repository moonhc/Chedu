import sqlite3
from flask import render_template, request, url_for, redirect, g, jsonify
from flask_socketio import send
from app import app, socketio

#############################
# DATABSE Wrapper functions #
#############################

# Initialize database
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

# Connect to database
def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = make_dicts
    return rv

# Make tuple to dictionary
def make_dicts(cur, row):
    return dict((cur.description[idx][0], value)
                    for idx, value in enumerate(row))

# Get the connection to database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_db()
    return db

# Query wrapper function
def query_db(query, args=(), one=False):
    cursor = get_db().execute(query, args)
    rv = cursor.fetchall()
    cursor.close()
    return (rv[0] if rv else None) if one else rv

# Close the connection to database
def close_db():
    with app.app_context:
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

# Request error handling
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#############################
#           Routing         #
#############################

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
def upload():
    return 'upload'

@app.route('/chat/<passcode>')
def chat(passcode, uname=None):
    if passcode == None :
        return error_handling()
    return render_template('chedu.html', passcode=passcode, uname=uname, message=None,
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
