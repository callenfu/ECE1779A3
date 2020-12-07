from flask import render_template,redirect,session,url_for
from app import app
from app.form import LoginForm


@app.route('/')
@app.route('/index')
def index():
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return redirect('home')
    # User is not loggedin redirect to login pa ge
    return render_template('index.html', title='Welcome Page')

@app.route('/home')
def home():
    if "loggedin" in session:
        # User is loggedin show them the homeadmin page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    else:
        return redirect(url_for('login'))