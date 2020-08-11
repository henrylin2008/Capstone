import os
import json
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy

database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))

db = SQLAlchemy()


def setup_db(app):
    """
    setup_db(app)
        binds a flask application and a SQLAlchemy service
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


def db_drop_and_create_all():
    """
    db_drop_and_create_all()
        drops the database tables and starts fresh
        can be used to initialize a clean database
        !!NOTE you can change the database_filename variable to have multiple verisons of a database
    """
    db.drop_all()
    db.create_all()


class Movie(db.Model):
    """
    Movie:
    a persistent movie entity, extends the base SQLAlchemy Model
    """
    __tablename__ = 'movies'
    # Auto-incrementing, unique primary key
    id = Column(Integer, primary_key=True)
    # String Title
    title = Column(String(80), unique=False)
    release = Column(db.Date)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        delete()
            deletes a new model into a database
            the model must exist in the database
            EXAMPLE
                drink = Drink(title=req_title, recipe=req_recipe)
                drink.delete()
        """
        db.session.delete(self)
        db.session.commit()

    def update(self):
        """
        update()
            updates a new model into a database
            the model must exist in the database
            EXAMPLE
                drink = Drink.query.filter(Drink.id == id).one_or_none()
                drink.title = 'Black Coffee'
                drink.update()
        """
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())


class Actor(db.Model):
    """
    Actors:
    a persistent actors entity, extends the base SQLAlchemy Model
    """
    __tablename__ = 'actors'
    # Auto-incrementing, unique primary key
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    # String Title
    name = Column(String(80), unique=False)
    gender = Column(String)
    age = Column(Integer)

    def insert(self):
        """
        insert()
            inserts a new model into a database
            the model must have a unique name
            the model must have a unique id or null id
            EXAMPLE
                drink = Drink(title=req_title, recipe=req_recipe)
                drink.insert()
        """
        db.session.add(self)
        db.session.commit()


    def delete(self):
        """
        delete()
            deletes a new model into a database
            the model must exist in the database
            EXAMPLE
                drink = Drink(title=req_title, recipe=req_recipe)
                drink.delete()
        """
        db.session.delete(self)
        db.session.commit()


    def update(self):
        """
        update()
            updates a new model into a database
            the model must exist in the database
            EXAMPLE
                drink = Drink.query.filter(Drink.id == id).one_or_none()
                drink.title = 'Black Coffee'
                drink.update()
        """
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())