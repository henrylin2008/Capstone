import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from .auth.auth import AuthError, requires_auth

# ---------------------------------------------------------------------#
# Initial setups
# ---------------------------------------------------------------------#
def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)

  # ---------------------------------------------------------------------#
  # Endpoints
  # ---------------------------------------------------------------------#
    ### movies ###
    @app.route('/movies', methods=['GET'])
    def retrieve_movies():

    @app.route('/movie/<int:movie_id>', methods=['GET'])
    def retrieve_movie_detail(payload, movie_id):

    @app.route('/movie', methods=['POST'])
    @requires_auth('post:movie')
    def add_movies(payload):

    @app.route('/movie/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movie')
    def update_movie(payload, movie_id):

    @app.route('/movie/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(payload, movie_id):



    ### Actors ###
    @app.route('/actors', methods=['GET'])
    def retrieve_actors():

    @app.route('/actor/<int:actor_id>', methods=['GET'])
    def retrieve_a_movie(payload, actor_id):

    @app.route('/actor', methods=['POST'])
    @requires_auth('post:actor')
    def add_movies(payload):

    @app.route('/actor/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actor')
    def update_movie(payload, actor_id):

    @app.route('/actor/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_movie(payload, actor_id):


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



app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)