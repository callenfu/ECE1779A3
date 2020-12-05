from flask import Flask
from app.database import UserTable
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.secret_key = 'ece1779a1'
from app import view
from app import login
from app import imageUpload

#app.run('0.0.0.0',5000,debug=True)