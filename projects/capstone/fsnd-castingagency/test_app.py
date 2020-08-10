import os
import unittest
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, db, Movie, Actor

TEST_DATABASE_URL = os.environ['TEST_DATABASE_URL']
CASTING_ASSISTANT_TOKEN = os.environ['CASTING_ASSISTANT_TOKEN']
CASTING_DIRECTOR_TOKEN = os.environ['CASTING_DIRECTOR_TOKEN']
EXECUTIVE_PRODUCER_TOKEN = os.environ['EXECUTIVE_PRODUCER_TOKEN']


class UnitTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app = create_app()
        cls.client = app.test_client
        setup_db(app, TEST_DATABASE_URL)

        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.drop_all()
        pass

    def authHeader(self, token):
        return {
            "Authorization": "Bearer {}".format(token)
        }

    new_movie = {
        'title': 'Schmovie',
        'release_date': '2020-01-14'
    }

    updated_movie = {
        'release_date': '2021-03-30'
    }

    new_actor = {
        'name': 'Dee Dringle',
        'age': 33,
        'gender': 'Female'
    }

    updated_actor = {
        'age': 34
    }

    # GET Tests

    def test1_get_movies(self):
        res = self.client().get(
            '/movies',
            headers=self.authHeader(
                CASTING_ASSISTANT_TOKEN
            ))
        self.assertEqual(res.status_code, 200)
        self.assertTrue('movies' in res.json)

    def test1_get_movies_authorization_header_missing(self):
        res = self.client().get('/movies')
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.json['message']['code'],
                         'authorization_header_missing')

    def test1_get_actors(self):
        res = self.client().get(
            '/actors',
            headers=self.authHeader(
                CASTING_ASSISTANT_TOKEN
            ))
        self.assertEqual(res.status_code, 200)
        self.assertTrue('actors' in res.json)

    def test1_get_actors_invalid_header(self):
        res = self.client().get('/actors', headers={
            "Authorization": "scheme token"
        })
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.json['message']['code'], 'invalid_header')

    # POST Tests

    def test2_create_movie(self):
        res = self.client().post(
            '/movies',
            json=self.new_movie,
            headers=self.authHeader(
                EXECUTIVE_PRODUCER_TOKEN
            ))
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json['success'])

    def test2_create_movie_invalid_json(self):
        res = self.client().post(
            '/movies',
            json={'this': 'is_bad'},
            headers=self.authHeader(
                EXECUTIVE_PRODUCER_TOKEN
            ))
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json['message'], 'Bad Request')

    def test2_create_movie_unauthorized(self):
        res = self.client().post(
            '/movies',
            json=self.new_movie,
            headers=self.authHeader(
                CASTING_DIRECTOR_TOKEN
            )
        )
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.json['message']['code'], 'unauthorized')

    def test2_create_actor(self):
        res = self.client().post(
            '/actors',
            json=self.new_actor,
            headers=self.authHeader(
                CASTING_DIRECTOR_TOKEN
            ))
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json['success'])

    def test2_create_actor_invalid_json(self):
        res = self.client().post(
            '/actors',
            json={'this': 'is_bad'},
            headers=self.authHeader(
                CASTING_DIRECTOR_TOKEN
            ))
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json['message'], 'Bad Request')

    def test2_create_actor_unauthorized(self):
        res = self.client().post(
            '/actors',
            json=self.new_actor,
            headers=self.authHeader(
                CASTING_ASSISTANT_TOKEN
            ))
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.json['message']['code'], 'unauthorized')

    # PATCH Tests

    def test3_update_movie(self):
        res = self.client().patch(
            '/movies/1',
            json=self.updated_movie,
            headers=self.authHeader(
                CASTING_DIRECTOR_TOKEN
            ))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json['movie']['release_date'],
                         self.updated_movie['release_date'])

    def test3_update_movie_not_found(self):
        res = self.client().patch(
            '/movies/2',
            json=self.updated_movie,
            headers=self.authHeader(
                CASTING_DIRECTOR_TOKEN
            ))
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.json['message'], 'Not Found')

    def test3_update_movie_unauthorized(self):
        res = self.client().patch(
            '/movies/1',
            json=self.updated_movie,
            headers=self.authHeader(
                CASTING_ASSISTANT_TOKEN
            ))
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.json['message']['code'], 'unauthorized')

    def test3_update_actor(self):
        res = self.client().patch(
            '/actors/1',
            json=self.updated_actor,
            headers=self.authHeader(
                CASTING_DIRECTOR_TOKEN
            ))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json['actor']['age'], self.updated_actor['age'])

    def test3_update_actor_not_found(self):
        res = self.client().patch(
            '/actors/2',
            json=self.updated_actor,
            headers=self.authHeader(
                CASTING_DIRECTOR_TOKEN
            ))
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.json['message'], 'Not Found')

    def test3_update_actor_unauthorized(self):
        res = self.client().patch(
            '/actors/1',
            json=self.updated_actor,
            headers=self.authHeader(
                CASTING_ASSISTANT_TOKEN
            ))
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.json['message']['code'], 'unauthorized')

    # DELETE Tests

    def test4_delete_movie(self):
        res = self.client().delete(
            '/movies/1',
            headers=self.authHeader(
                EXECUTIVE_PRODUCER_TOKEN
            ))
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json['success'])

    def test4_delete_movie_not_found(self):
        res = self.client().delete(
            '/movies/2',
            headers=self.authHeader(
                EXECUTIVE_PRODUCER_TOKEN
            ))
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.json['message'], 'Not Found')

    def test4_delete_movie_unauthorized(self):
        res = self.client().delete(
            '/movies/1',
            headers=self.authHeader(
                CASTING_DIRECTOR_TOKEN
            ))
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.json['message']['code'], 'unauthorized')

    def test4_delete_actor(self):
        res = self.client().delete(
            '/actors/1',
            headers=self.authHeader(
                CASTING_DIRECTOR_TOKEN
            ))
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json['success'])

    def test4_delete_actor_not_found(self):
        res = self.client().delete(
            '/actors/2',
            headers=self.authHeader(
                CASTING_DIRECTOR_TOKEN
            ))
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.json['message'], 'Not Found')

    def test4_delete_actor_unauthorized(self):
        res = self.client().delete(
            '/actors/1',
            headers=self.authHeader(
                CASTING_ASSISTANT_TOKEN
            ))
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.json['message']['code'], 'unauthorized')


if __name__ == "__main__":
    unittest.main()
