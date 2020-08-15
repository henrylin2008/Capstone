import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from .database.models import setup_db, Actor, Movie
from .auth.auth import AuthError, requires_auth
import json


# ---------------------------------------------------------------------#
# Initial setups
# ---------------------------------------------------------------------#
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        """Setting Access-Control-allow
      Parameters:
          response: an instance of response_class
      Return:
          response object with Access-Control-Allow
      """
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    # ---------------------------------------------------------------------#
    # Endpoints
    # ---------------------------------------------------------------------#

    @app.route('/')
    def index():
        return jsonify('Welcome to Casting Agency!')

    # -- movies endpoints -- #
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def retrieve_movies(payload):
        movie_query = Movie.query.all()
        if len(movie_query) == 0:
            abort(404)

        movies_format = [movie.format() for movie in movie_query]
        return jsonify({
            'success': True,
            'movies': movies_format
        }), 200

    @app.route('/movie/<int:movie_id>', methods=['GET'])
    @requires_auth('get:movie')
    def retrieve_movie_detail(payload, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404, {'message': 'Movie with id {} not found in database.'.format(movie_id)})

        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 200

    @app.route('/movie', methods=['POST'])
    @requires_auth('post:movie')
    def add_movies(payload):
        body = request.get_json()
        title = body.get('title', None)
        release_date = body.get('release_date', None)

        if not title or not release_date:
            abort(422, {"message": "Title and release_date are required"})

        try:
            movie = Movie(title=title, release_date=release_date)
            movie.insert()
            new_movie = Movie.query.get(movie.id)
            new_movie = new_movie.format()

            return jsonify({
                'success': True,
                'movie': movie.id,
                'new movie': new_movie
            }), 200
        except:
            abort(422)

    @app.route('/movie/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movie')
    def update_movie(payload, movie_id):
        body = request.get_json()
        title = body.get('title', None)
        release_date = body.get('release_date', None)

        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if not movie:
            abort(404, {'message': 'Movie with id {} not found in database.'.format(movie_id)})

        try:
            if title:
                movie.title = title
            if release_date:
                movie.release_date = release_date

            movie.update()

        except:
            abort(422)

        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 200

    @app.route('/movie/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(payload, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404, {'message': 'Movie with id {} not found in the database.'.format(movie_id)})

        try:
            movie.delete()
        except:
            abort(422)

            return jsonify({
                'success': True,
                'delete': movie_id,
                'message': "Movie has been deleted"
            }), 200

    # -- Actors endpoints -- #
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def retrieve_actors():
        actor_query = Actor.query.all()
        if len(actor_query) == 0:
            abort(404)

        actors_format = [actor.format() for actor in actor_query]
        return jsonify({
            'success': True,
            'actors': actors_format
        }), 200

    @app.route('/actor/<int:actor_id>', methods=['GET'])
    @requires_auth('get:actor')
    def retrieve_an_actor(payload, actor_id):
        actor_query = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor_query is None:
            abort(404, {'message': 'Actor with id {} not found in database.'.format(actor_id)})

        return jsonify({
            'success': True,
            'actor': actor_query.format()
        }), 200

    @app.route('/actor', methods=['POST'])
    @requires_auth('post:actor')
    def add_actor(payload):
        body = request.get_json()
        name = body.get('name')
        age = body.get('age')
        gender = body.get('gender')

        if not name or not age or not gender:
            abort(422, {"message": "Name, age, and gender are required"})

        try:
            actor = Actor(name=name, age=age, gender=gender)
            actor.insert()
            new_actor = Actor.query.get(actor.id)
            new_actor = new_actor.format()
        except:
            abort(422)

        return jsonify({
            'success': True,
            'movie': actor.id,
            'new actor': new_actor
        }), 200

    @app.route('/actor/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actor')
    def update_actor(payload, actor_id):
        body = request.get_json()
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)

        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if not actor:
            abort(404, {'message': 'Actor with id {} not found in database.'.format(actor_id)})

        try:
            if name:
                actor.name = name
            if age:
                actor.age = age
            if gender:
                actor.gender = gender

            actor.update()
        except:
            abort(422)

        return jsonify({
            'success': True,
            'actor': actor.format()
        }), 200

    @app.route('/actor/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(payload, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404, {'message': 'Movie with id {} not found in the database.'.format(actor_id)})

        try:
            actor.delete()
        except:
            abort(422)

            return jsonify({
                'success': True,
                'delete': actor_id,
                'message': "Actor has been deleted"
            }), 200

    # ---------------------------------------------------------------------#
    # Error Handlers
    # ---------------------------------------------------------------------#

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(401)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Not authorized"
        }), 404

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal server error"
        }), 500

    @app.errorhandler(AuthError)
    def handle_auth_error(error):
        """
    Receive the raised authorization error and propagates it as response
    """
        response = jsonify(error.error)
        response.status_code = error.status_code

        return response

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
