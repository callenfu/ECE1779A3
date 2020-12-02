from flask import Flask

app = Flask(__name__)

from app import view

app.run('0.0.0.0',5000,debug=True)

