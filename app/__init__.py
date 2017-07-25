from __future__ import with_statement
from contextlib import closing
import sqlite3
from flask import Flask
from flask_socketio import SocketIO

# Configuration for database
DATABASE = '/home/chedu/Chedu/app/database/chedu.db'
DEBUG = False
SECRET_KEY = "Yellow Slug"
USERNAME = "Chedu"
PASSWORD = "slug123"

# Configuration for files
UPLOAD_FOLDER = '/home/chedu/Chedu/app/tmp_files/'
ALLOWED_EXTENSIONS = set(['ppt', 'pptx', 'xlxx', 'xlx', 'doc', 'docx', 'pdf'])

# Configuration for viewer
VIEWER_DEFAULT = 'https://view.officeapps.live.com/op/embed.aspx?src=http://ucscchedu.click/uploads/'
VIEWER_PDF = 'http://ucscchedu.click/uploads/'

# Create application
app = Flask(__name__)
app.config.from_object(__name__)
socketio = SocketIO(app)

from app import routes
