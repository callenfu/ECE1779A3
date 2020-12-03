from app import app
from flask import render_template, request, session, redirect, url_for, flash
from app.database import  UserTable
# from flask_mail import Message
from app.form import LoginForm
# , ChangePassword, ResetPassword, AddUserForm
from werkzeug.security import generate_password_hash, check_password_hash
# from app.email import send_password_reset_email

usertable = UserTable()

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Controller that display the login page.controller that display the imageView page.
    This controller will assert if user is already logged in or not.
    If yes, it will redirect to home page.
    If no, it will show the login page and let user input username and password.
    Once user submit the username and password, it will go to dababase and verify them.
    If login success, user id, username, admin_auth will be save in session
    account: assert if username is in database.
    """
    form = LoginForm()
    if request.method == "GET":
        return render_template('login.html', title='Sign In', form=form)
    if request.method == "POST":
        if 'loggedin' in session:
            return redirect(url_for('index'))
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            account = usertable.check_item("username", username)
            if account == None:
                flash('Invalid username or password')
                return redirect(url_for('login'))
            else:
                if check_password_hash(str(account['password_hash']), password):
                    session['loggedin'] = True
                    session['username'] = account['username']
                    session['admin_auth'] = account['admin_auth']
                    flash('Login successfully!')
                    return redirect(url_for('index'))
            flash('Invalid username or password')
            return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    session.pop('message', None)
    session.pop('admin_auth', None)
    """Controller pop the login status and user information in session, then redirect to index page"""
    return redirect(url_for('index'))

