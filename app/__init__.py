from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

# Initialize extensions
bcrypt = Bcrypt()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '\xed\xe3\x96}2\x7f\x15S\xfc\xcc\x01}\x14\xc6\xe4V\x9c\xf5W\x17\xc0\xf6L\xdb'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meteormate.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)

    # Register blueprints
    from .routes import bp
    app.register_blueprint(bp)

    with app.app_context():
        db.create_all()

    return app
