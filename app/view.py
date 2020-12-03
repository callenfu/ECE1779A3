from flask import render_template
from app import app
from app.form import LoginForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')