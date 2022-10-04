from flask import render_template, url_for
from ccr_dashboard import app

@app.route('/')
def index():
    return render_template('layout.html',title='Dashboard')