from flask import Flask,session
import os
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)


app.config['SECRET_KEY'] = 'fe8510d29c8f605c2c64b808b44ed0f6227d1e1e0653681e'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///grocery.db"
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

app.app_context().push()

from app_grocery import links