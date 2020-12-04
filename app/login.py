from app import app
from flask import render_template, request, session, redirect, url_for, flash
from app.database import  UserTable
from flask_mail import Message
from app.form import LoginForm, ChangePassword,RegisterForm, ResetPassword
from werkzeug.security import generate_password_hash, check_password_hash
from app.email import send_password_reset_email
import string, random


usertable = UserTable()

def generate_password():
    """method generate password will random a 10-length-string with numbers and letters,
    it will be used in reset_password function.
    """
    chars = string.ascii_letters + string.digits
    key = random.sample(chars, 10)
    keys = "".join(key)
    return keys

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
            return redirect(url_for('home'))
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
                    return redirect(url_for('home'))
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

@app.route('/change_my_password', methods=['POST', 'GET'])
def change_my_password():
    """Controller is allow user to change their password if they have valid username and password.
    It will generate the new password hash and write into the database.
    If username not exist, or wrong password, controller will not allow user change password.
     """
    form = ChangePassword()
    if request.method == 'GET':
        return render_template('changemypassword.html', form=form)
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        old_password = form.password.data
        new_password_hash = generate_password_hash(form.password1.data)
        account = usertable.check_item("username", username)
        if account is not None:
            if check_password_hash(str(account['password_hash']), old_password):
                usertable.update_password_username(username, new_password_hash)
                flash('Your password has been changed')
                return redirect(url_for('login'))
            else:
                flash('Invalid username or password')
                return redirect(url_for('change_my_password'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('change_my_password'))
    else:
        return render_template('changemypassword.html', form=form)


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    """controller will allow admin user to add new user.
    It will assert if user want to create a new account. if it is normal user, it will redirect to login page
    When admin add new user, if same username or email in database, it will refuse to create new user
    Admin also allow to create another admin by input admin_auth True"""
    form = RegisterForm()
    if request.method == "GET":
        return render_template('adduser.html', title='Add New User', form=form)
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password1.data
        email = form.email.data
        account = usertable.check_item("username", username)
        if account is not None:
            flash('This User name or Email is existing')
            return redirect(url_for('sign_up'))
        else:
            usertable.add_user(username,password,email)
            flash("You have add a new user successfully")
            return redirect(url_for('sign_up'))


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    """Controller that display the reset_password page. Only user_email is needed to be input.
    Controller will validate the email in database and generate a new password 10-lenght-random string.
    Then it will try to send a email with new password to user's mailbox by gmail.
    Email template is email.txt"""
    form = ResetPassword()
    if form.validate_on_submit():
        user_email = form.email.data
        mail_exist = usertable.check_item('email',user_email)
        if mail_exist is not None:
            new_password = generate_password()
            new_password_hash = generate_password_hash(new_password)
            username = mail_exist['username']
            usertable.update_password_username(username,new_password_hash)
            flash('Your new password has been sent to your mailbox')
            redirect('login')
            send_password_reset_email(user_email, new_password)
            return redirect(url_for('login'))
        else:
            flash('This email address is not registered')
            return redirect('reset_password')
    return render_template('resetpassword.html', form=form)