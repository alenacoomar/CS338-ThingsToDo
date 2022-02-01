from flask import Flask
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)
manager = Manager(app)

app.config.from_pyfile("config/base_setting.py")


db = SQLAlchemy(app)

