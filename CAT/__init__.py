from flask import Flask
from flask_mongoengine import MongoEngine

async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ebe8b8c7ba526c2846a3213c6e45135b'
app.config["MONGODB_SETTINGS"] = [
    {
        "db": "rf_cascade",
        "host": "localhost",
        "port": 27017,
        "alias": "default",
    }
]
db = MongoEngine(app)

from CAT import routes