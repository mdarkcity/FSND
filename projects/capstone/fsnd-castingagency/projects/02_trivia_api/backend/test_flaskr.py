import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {
            'question': 'Will this work?',
            'answer': 'Maybe',
            'difficulty': 1,
            'category': 1
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories(self):
        resp = self.client().get('/categories')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.json['categories']))

    def test_get_categories_by_index_not_found(self):
        resp = self.client().get('/categories/1')
        self.assertEqual(resp.status_code, 404)
        self.assertTrue(resp.json['error'])
        self.assertEqual(resp.json['message'], 'Not Found')

    def test_get_questions(self):
        resp = self.client().get('/questions')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json['total_questions'])

    def test_get_questions_invalid_page(self):
        resp = self.client().get('/questions?page=0')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json['questions']), 0)

    def test_get_questions_by_index_not_allowed(self):
        resp = self.client().get('/questions/1')
        self.assertEqual(resp.status_code, 405)
        self.assertTrue(resp.json['error'])
        self.assertEqual(resp.json['message'], 'Method Not Allowed')

    def test_delete_question(self):
        new_question = self.client().post(
            '/questions', json=self.new_question
        ).json
        resp = self.client().delete(
            '/questions/{}'.format(new_question['question_id']))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['success'], True)

    def test_delete_question_not_found(self):
        resp = self.client().delete('/questions/0')
        self.assertEqual(resp.status_code, 404)
        self.assertTrue(resp.json['error'])
        self.assertEqual(resp.json['message'], 'Not Found')

    def test_add_questions(self):
        resp = self.client().post('/questions', json=self.new_question)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['success'], True)
        self.assertTrue(resp.json['question_id'])

    def test_add_questions_no_body(self):
        resp = self.client().post('/questions')
        self.assertEqual(resp.status_code, 400)
        self.assertTrue(resp.json['error'])
        self.assertEqual(resp.json['message'], 'Bad Request')

    def test_search_questions(self):
        resp = self.client().post('/questions/search',
                                  json={'search_term': 'which'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json['total_questions'])

    def test_get_questions_by_categories(self):
        resp = self.client().get('/categories/1/questions')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.json['questions']))

    def test_play_quiz(self):
        quiz_request_body = {
            'previous_questions': [],
            'quiz_category': '0'
        }
        resp = self.client().post('/quizzes', json=quiz_request_body)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json['question'])

    def test_play_quiz_invalid_category(self):
        quiz_request_body = {
            'previous_questions': [],
            'quiz_category': '99'
        }
        resp = self.client().post('/quizzes', json=quiz_request_body)
        self.assertEqual(resp.status_code, 200)
        self.assertIsNone(resp.json['question'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
