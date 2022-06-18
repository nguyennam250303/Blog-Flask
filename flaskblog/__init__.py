from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
app = Flask(__name__)

SECRET_KEY = os.urandom(12)

app.config["SECRET_KEY"] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///flask_blog.db"

db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = "login_page"
login.login_message_category = "danger"
from flaskblog import models
from flaskblog import routes

