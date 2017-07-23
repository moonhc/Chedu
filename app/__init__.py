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

# Create application
app = Flask(__name__)
app.config.from_object(__name__)
socketio = SocketIO(app)

from app import routes
