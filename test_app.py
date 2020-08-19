import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from .app import create_app
from .database.models import setup_db


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    # ---------------------------------------------------------------------#
    # Initial setups
    # ---------------------------------------------------------------------#
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.casting_assistant = os.getenv('CASTING_ASSISTANT')
        self.casting_director = os.getenv('CASTING_DIRECTOR')
        self.executive_producer = os.getenv('EXECUTIVE_PRODUCER')

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    # def tearDown(self):
    #     """Executed after reach test"""
    #     pass

    # ---------------------------------------------------------------------#
    # Test Movie endpoints
    # ---------------------------------------------------------------------#
    def test_get_all_movies(self):
        """Test case for retrieving movies function"""
        response = self.client().get(
            '/movies',
            headers={
                "Authorization": "Bearer {}".format(
                    self.casting_assistant)})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_get_a_movie(self):
        """Test case for retrieving a movie function"""
        response = self.client().get(
            "/movie/1",
            headers={
                "Authorization": "Bearer {}".format(
                    self.casting_director)})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_400_requesting_beyond_valid_movie_id(self):
        """Test case for 400 sending request beyond available movies"""
        response = self.client().get(
            '/movie/1000',
            headers={
                "Authorization": "Bearer {}".format(
                    self.casting_director)})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'Please provide a valid movie id')

    def test_add_movie(self):
        """Test case to add a new movie"""
        response = self.client().post(
            '/movie',
            json={
                "title": "new movie",
                "release_date": "Mon, 14 Jul 2008 01:01:00 GMT",
                "actor_id": 3},
            headers={
                "Authorization": "Bearer {}".format(
                    self.casting_director)})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_400_sent_invalid_data_add_movie(self):
        response = self.client().post(
            '/movie',
            json={
                "title": "new movie",
                "release_date": "Mon, 14 Jul 2008 01:01:00 GMT",
            },
            headers={
                "Authorization": "Bearer {}".format(
                    self.casting_director)})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(
            data['message'],
            'title, release_date, and actor_id are required!')

    def test_update_movie(self):
        """Test case to update a movie"""
        response = self.client().patch(
            '/movie/10',
            json={
                "title": "update movie",
                "release_date": "Mon, 14 Jul 2008 01:01:00 GMT",
                "actor_id": 5},
            headers={
                "Authorization": "Bearer {}".format(
                    self.casting_director)})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_delete_movie(self):
        """Test case to delete a movie"""
        response = self.client().delete(
            '/movie/5',
            headers={
                "Authorization": "Bearer {}".format(
                    self.executive_producer)})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 5)

    def test_400_sent_deleting_non_existing_movie(self):
        """Test case for deleting a non-existing movie"""
        response = self.client().delete(
            '/movie/1000',
            headers={
                "Authorization": "Bearer {}".format(
                    self.executive_producer)})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'Invalid movie id')

    # ---------------------------------------------------------------------#
    # Test Actor endpoints
    # ---------------------------------------------------------------------#
    def test_get_all_actors(self):
        """Test case for retrieving all actors function"""
        response = self.client().get(
            '/actors',
            headers={
                "Authorization": "Bearer {}".format(
                    self.casting_assistant)})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_get_a_actor(self):
        """Test case for retrieving an actor function"""
        response = self.client().get(
            "/actor/1",
            headers={
                "Authorization": "Bearer {}".format(
                    self.casting_director)})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_400_requesting_beyond_valid_movie_id(self):
        """Test case for 400 sending request beyond available movies"""
        response = self.client().get(
            '/actor/1000',
            headers={
                "Authorization": "Bearer {}".format(
                    self.casting_director)})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'Invalid actor id')

    def test_add_actor(self):
        """Test case to add a new actor"""
        response = self.client().post(
            '/actor',
            json={
                "name": "Bruce Lee",
                "gender": "male",
                "age": 33},
            headers={
                "Authorization": "Bearer {}".format(
                    self.casting_director)})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_400_sent_invalid_data_add_actor(self):
        """Test case of adding a new actor with invalid data"""
        response = self.client().post(
            '/actor',
            json={
                "name": "Bruce Lee",
                "gender": "male",
            },
            headers={
                "Authorization": "Bearer {}".format(
                    self.casting_director)})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(
            data['message'],
            'name, age, and gender are required!')

    def test_update_actor(self):
        """Test case to update a movie"""
        response = self.client().patch(
            '/actor/5',
            json={
                "name": "JJ",
                "age": 24,
                "gender": "male"},
            headers={
                "Authorization": "Bearer {}".format(
                    self.casting_director)})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_delete_actor(self):
        """Test case to delete an actor"""
        response = self.client().delete(
            '/actor/5',
            headers={
                "Authorization": "Bearer {}".format(
                    self.executive_producer)})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 5)
        self.assertEqual(data['message'], 'Actor has been deleted')

    def test_400_sent_deleting_non_existing_actor(self):
        """Test case for deleting a non-existing movie"""
        response = self.client().delete(
            '/actor/1000',
            headers={
                "Authorization": "Bearer {}".format(
                    self.executive_producer)})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'Invalid actor id')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
