import sqlite3, os, random, string, pytz
from datetime import datetime
from flask import render_template, request, url_for, redirect, g, jsonify, send_from_directory
from flask_socketio import send, join_room, emit
from werkzeug import secure_filename
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

# Simple query wrapper function
def query_db(query, args=(), one=False):
    cursor = get_db().execute(query, args)
    rv = cursor.fetchall()
    cursor.close()
    return (rv[0] if rv else None) if one else rv

# Insert wrapper function
def insert_db(table_name, args):
    query = 'insert into ' + table_name
    if table_name == 'files' and len(args) == 3:
        query += ' values (?, ?, ?)'
    elif table_name == 'chat_log' and len(args) == 4:
        query += ' (passcode, user_email, message, chat_date) values (?, ?, ?, ?)'
    else:
        return error_handling()
    db = get_db()
    db.execute(query, args)
    db.commit()

# Close the connection to database
def close_db():
    with app.app_context:
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

#############################
#      Useful functions     #
#############################

def make_passcode():
    while True:
        passcode = ''.join(random.choice(string.letters) for _ in xrange(8))
        if validate_passcode(passcode):
            return passcode

def validate_passcode(passcode):
    if passcode is None:
        return False

    files_entry = query_db('select * from files where passcode = ?', [passcode], one=True)
    if files_entry is None:
        return True
    return False

#############################
#           Routing         #
#############################

# Render login page.
@app.route('/')
def index():
    #tmpDict = {}
    #tmpDict['userName'] = 'MoonHC'
    return render_template('Login.html')#, **tmpDict)

# Validate PASSCODE and email. Then redirect to ppt view page.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        uname = email.split('@')[0] if '@' in email else email
        return redirect(url_for('chat', passcode=request.form['passcode'], uname=uname))
    else:
        return error_handling()

# Check the file type which was set previously in configuration (app.config).
def allowed_file(filename):
    return ('.' in filename) and (filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS'])

# HTTP request url for uploding a file.
@app.route('/files', methods=['GET', 'POST'])
def upload_file():
    try:
        if request.method == 'POST':
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                passcode = make_passcode()
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], passcode+filename))
                timezone = pytz.timezone('US/Pacific')
                current_time = datetime.now(timezone).strftime('20%y-%m-%d')
                insert_db('files', [passcode, filename, current_time])
                return redirect(url_for('chat', passcode=passcode, uname='Owner'))
        return redirect(url_for('index'))
    except:
        return error_handling()

# Give a access for uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

# Render chat page with correct password.
@app.route('/chat/<passcode>/<uname>')
def chat(passcode, uname):
    if validate_passcode(passcode):
        return error_handling()

    file_info = query_db('select * from files where passcode = ?', [passcode], one=True)
    filename = '.'.join(file_info['file_name'].split('.')[0:-1])
    viewer = app.config['VIEWER_PDF'] if 'pdf' in file_info['file_name'].split('.')[-1] else app.config['VIEWER_DEFAULT']
    filename = filename[0].upper() + filename[1:]
    return render_template('chedu.html', passcode=passcode, uname=uname,
                            filename=filename, file_url=file_info['file_name'], viewer=viewer)

# Render decription page.
@app.route('/about')
def show_about():
    return render_template('about.html')

# Request error handling
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Socket for message. After recieve message from 'msg'
# and publish to all the users who see the same ppt.
@socketio.on('message')
def message_handler(data):
    room = data.pop('room')
    timezone = pytz.timezone('US/Pacific')
    current_time = datetime.now(timezone).strftime('%H:%M')
    data['time'] = current_time
    send(data, room=room)

@socketio.on('join')
def on_join(data):
    join_room(data['room'])
    send({'uname': data['uname'], 'type': 'new'}, room=data['room'])

# Default error handling function
def error_handling():
    return "Not vaild access!"
