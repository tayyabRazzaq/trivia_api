"""Module for tests."""

import unittest

from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from flaskr.constants import (
    ERROR_MESSAGES, STATUS_BAD_REQUEST, STATUS_CREATED, STATUS_FORBIDDEN, STATUS_METHOD_NOT_ALLOWED,
    STATUS_NOT_FOUND, STATUS_NO_CONTENT, STATUS_OK, STATUS_UNAUTHORIZED, STATUS_UNPROCESSABLE_ENTITY
)

from models import get_database_path, setup_db


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case."""

    def setUp(self):
        """
        Define test variables and initialize app.

        :return:
        """
        self.app = create_app()
        self.client = self.app.test_client()
        self.database_name = "trivia_test"
        self.database_path = get_database_path(self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def test_get_categories_success(self):
        """
        Success test case for get categories route.

        :return:
        """
        response = self.client.get('/categories')
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_OK)
        self.assertEqual(json_data.get('success'), True)

    def test_get_categories_failed(self):
        """
        Fail test case for get categories route.

        :return:
        """
        response = self.client.post('/categories')
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_METHOD_NOT_ALLOWED)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(json_data.get('message'), ERROR_MESSAGES[STATUS_METHOD_NOT_ALLOWED])

    def test_get_questions_success(self):
        """
        Success case for get questions.

        :return:
        """
        response = self.client.get('/questions')
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_OK)
        self.assertEqual(json_data.get('success'), True)

    def test_get_questions_failed(self):
        """
        Fail case for get questions.

        :return:
        """
        response = self.client.get('/questions?page=-1000')
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_NOT_FOUND)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(json_data.get('message'), ERROR_MESSAGES[STATUS_NOT_FOUND])

    def test_delete_question_success(self):
        """
        Success case of delete question test case.

        :return:
        """
        response = self.client.delete('/questions/15')
        self.assertEqual(response.status_code, STATUS_NO_CONTENT)

    def test_delete_question_failed_method_not_allowed(self):
        """
        Method not allowed failed case of delete question test case.

        :return:
        """
        response = self.client.get('/questions/10')
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_METHOD_NOT_ALLOWED)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(json_data.get('message'), ERROR_MESSAGES[STATUS_METHOD_NOT_ALLOWED])

    def test_delete_question_failed_not_found(self):
        """
        Not found failed case of delete question test case.

        :return:
        """
        response = self.client.delete('/questions/-1000')
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_NOT_FOUND)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(json_data.get('message'), ERROR_MESSAGES[STATUS_NOT_FOUND])

    def test_add_question_success(self):
        """
        Success case of add question test case.

        :return:
        """
        question = {
            "question": "Test 1",
            "answer": "Answer 1",
            "category": 1,
            "difficulty": 1
        }
        response = self.client.post('/questions', json=question)
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_CREATED)
        self.assertEqual(json_data.get('success'), True)

    def test_add_question_failed_method_not_allowed(self):
        """
        Fail case of add question test case with method not allowed error.

        :return:
        """
        response = self.client.put('/questions', json={})
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_METHOD_NOT_ALLOWED)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(json_data.get('message'), ERROR_MESSAGES[STATUS_METHOD_NOT_ALLOWED])

    def test_add_question_failed_bad_request(self):
        """
        Fail case of add question test case with bad request error.
        :return:
        """
        response = self.client.post('/questions', json={})
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_BAD_REQUEST)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(json_data.get('message'), ERROR_MESSAGES[STATUS_BAD_REQUEST])

    def test_search_questions_success(self):
        """
        Success case of search questions api.

        :return:
        """
        data = {
            "searchTerm": "The"
        }
        response = self.client.post('/questions/filter', json=data)
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_OK)
        self.assertEqual(json_data.get('success'), True)

    def tearDown(self):
        """
        Execute after reach test.

        :return:
        """
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
