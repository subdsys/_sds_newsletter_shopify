from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, email):
        self.email = email
