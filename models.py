import os
import json
from flask_sqlalchemy import SQLAlchemy

DATABASE_URL = os.environ['DATABASE_URL']

db = SQLAlchemy()


def setup_db(app, database_url=DATABASE_URL):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class BaseModel():
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Movie(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.Date(), nullable=False)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def format(self):
        return {
            'title': self.title,
            'release_date': str(self.release_date)
        }

    def __repr__(self):
        return json.dumps(self.format())


class Actor(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String)

    def __init__(self, name, age, gender=None):
        self.name = name
        self.age = age
        self.gender = gender

    def format(self):
        return {
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

    def __repr__(self):
        return json.dumps(self.format())
