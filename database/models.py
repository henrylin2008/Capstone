import os
import json
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from flask_sqlalchemy import SQLAlchemy

db_name = "casting"
db_user = 'postgres'
db_host = 'localhost'
db_port = '5432'
database_path = "postgres://{}@{}:{}/{}".format(
    db_user,
    db_host,
    db_port,
    db_name)

db = SQLAlchemy()


def setup_db(app, db_path=database_path):
    """
    setup_db(app)
        binds a flask application and a SQLAlchemy service
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = db_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


def db_drop_and_create_all():
    """
    db_drop_and_create_all()
        drops the database tables and starts fresh
        can be used to initialize a clean database
    """
    db.drop_all()
    db.create_all()


class Movie(db.Model):
    """
    Movie:
    a persistent movie entity, extends the base SQLAlchemy Model
    """
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    release_date = Column(db.Date, nullable=False)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        """
        insert()
            inserts a new model into a database
            the model requires a unique id, releaseDate, and title
        """
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        update()
            updates a new model into a database
            the model must exist in the database
        """
        db.session.commit()

    def delete(self):
        """
        delete()
            deletes a new model into a database
            the model must exist in the database
        """
        db.session.delete(self)
        db.session.commit()

    def format(self):
        """
        format()
            output format that contains id, title, and release date
        """
        return {
            'id': self.id,
            'title': self.title,
            'release date': self.release_date
        }


class Actor(db.Model):
    """
    Actors:
    a persistent actors entity, extends the base SQLAlchemy Model
    """
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    gender = Column(String(8))
    age = Column(Integer)

    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.age = age

    def insert(self):
        """
        insert()
            inserts a new model into a database
            the model must have a unique name
            the model must have a unique id or null id
        """
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        update()
            updates a new model into a database
            the model must exist in the database
        """
        db.session.commit()

    def delete(self):
        """
        delete()
            deletes a new model into a database
            the model must exist in the database
        """
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'age': self.age
        }

