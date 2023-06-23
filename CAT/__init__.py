from flask import Flask
from flask_sqlalchemy import SQLAlchemy

async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ebe8b8c7ba526c2846a3213c6e45135b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from CAT import routes