from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = '\xed\xe3\x96}2\x7f\x15S\xfc\xcc\x01}\x14\xc6\xe4V\x9c\xf5W\x17\xc0\xf6L\xdb'

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meteormate.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Initialize Bcrypt for password hashing
bcrypt = Bcrypt()

from .routes import bp
app.register_blueprint(bp)
