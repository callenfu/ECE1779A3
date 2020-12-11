from flask import Flask
from app.database import DynamoDB
from flask_bootstrap import Bootstrap
from flask_mail import Mail


app = Flask(__name__)

app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'ece1779group@gmail.com',
    MAIL_PASSWORD = 'Toronto1779'
))
mail = Mail(app)
bootstrap = Bootstrap(app)
app.secret_key = 'ece1779a1'
from app import view
from app import login
from app import imageUpload
from app import email

# app.run('0.0.0.0',5000,debug=True)