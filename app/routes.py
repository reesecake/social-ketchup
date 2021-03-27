from flask import render_template
from flask_login import current_user

from api import app


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
