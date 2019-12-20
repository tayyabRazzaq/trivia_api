"""Module for tests."""

import unittest

from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from flaskr.constants import STATUS_OK, STATUS_METHOD_NOT_ALLOWED, STATUS_NOT_FOUND

from models import get_database_path, setup_db


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case."""

    def setUp(self):
        """
        Define test variables and initialize app.

        :return:
        """
        self.app = create_app()
        self.client = self.app.test_client
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
        response = self.client().get('/categories')
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_OK)
        self.assertEqual(json_data.get('success'), True)

    def test_get_categories_failed(self):
        """
        Fail test case for get categories route.

        :return:
        """
        response = self.client().post('/categories')
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_METHOD_NOT_ALLOWED)
        self.assertEqual(json_data.get('success'), False)

    def test_get_questions_success(self):
        response = self.client().get('/questions')
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
