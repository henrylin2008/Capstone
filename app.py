import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)


    @app.route('/movies', methods=['GET'])
    def retrieve_movies():

    @app.route('/movies', methods=['POST'])
    def add_movies():

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    def delete_movie(payload, movie_id):

    @app.route('/movie/<int:movie_id>', methods=['PATCH'])
    def update_movie(payload, movie_id):


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)