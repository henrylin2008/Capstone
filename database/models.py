import os
import json
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from flask_sqlalchemy import SQLAlchemy

# db_name = "casting"
# db_user = 'postgres'
# db_host = 'localhost'
# db_port = '5432'
# database_path = "postgres://{}@{}:{}/{}".format(
#     db_user,
#     db_host,
#     db_port,
#     db_name)
database_path = 'postgres://kzsscvnozhpwcl:4224bc447debc9d8b501be3bbce9373222d97ce2d2bff64b767b85e4a216d2ff@ec2-184-73-249-9.compute-1.amazonaws.com:5432/d27nosece0i7eb'
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
    release_date = Column(db.Date)
    actor_id = Column(Integer, ForeignKey('actors.id'))
    actors = relationship('Actor', backref=backref('movies', lazy=True))

    def __init__(self, title, release_date, actor_id):
        self.title = title
        self.release_date = release_date
        self.actor_id = actor_id

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
            'Title': self.title,
            'Release Date': self.release_date,
            'Movie ID': self.id,
            'Actor ID': self.actor_id,
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
            'Actor ID': self.id,
            'Name': self.name,
            'Gender': self.gender,
            'Age': self.age
        }
