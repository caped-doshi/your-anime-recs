from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Anime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    episodes = db.Column(db.Integer)
    rating = db.Column(db.Float)
    release_data = db.Column(db.DateTime(timezone=True), default=func.now())

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    #ratings = db.Column(db.PickleType())