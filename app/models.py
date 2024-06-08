from . import db,app

class User(db.Model):
    __tablename__ = 'user'  # Explicitly specify the table name
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    
with app.app_context():
        db.create_all()