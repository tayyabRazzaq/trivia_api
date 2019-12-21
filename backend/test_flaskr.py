"""Module for tests."""

import unittest

from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from flaskr.constants import (
    ERROR_MESSAGES, STATUS_BAD_REQUEST, STATUS_CREATED,
    STATUS_METHOD_NOT_ALLOWED, STATUS_NOT_FOUND, STATUS_NO_CONTENT, STATUS_OK,
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
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = get_database_path(self.database_name)
        setup_db(self.app, self.database_path)

        self.question = {
            "question": "Test 1",
            "answer": "Answer 1",
            "category": 1,
            "difficulty": 1
        }

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
        self.assertTrue(len(json_data.get('categories')))

    def test_get_categories_failed(self):
        """
        Fail test case for get categories route.

        :return:
        """
        response = self.client().post('/categories')
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_METHOD_NOT_ALLOWED)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(
            json_data.get('message'), ERROR_MESSAGES[STATUS_METHOD_NOT_ALLOWED]
        )

    def test_get_questions_success(self):
        """
        Success case for get questions.

        :return:
        """
        response = self.client().get('/questions')
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_OK)
        self.assertEqual(json_data.get('success'), True)
        self.assertTrue(len(json_data.get('categories')))
        self.assertTrue(len(json_data.get('questions')))
        self.assertTrue(json_data.get('total_questions'))

    def test_get_questions_failed(self):
        """
        Fail case for get questions.

        :return:
        """
        response = self.client().get('/questions?page=-1000')
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_NOT_FOUND)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(
            json_data.get('message'), ERROR_MESSAGES[STATUS_NOT_FOUND]
        )

    def test_delete_question_success(self):
        """
        Success case of delete question test case.

        :return:
        """
        response = self.client().post('/questions', json=self.question)
        json_data = response.get_json()
        response = self.client().delete(f'/questions/{json_data.get("id")}')
        self.assertEqual(response.status_code, STATUS_NO_CONTENT)

    def test_delete_question_failed_method_not_allowed(self):
        """
        Method not allowed failed case of delete question test case.

        :return:
        """
        response = self.client().get('/questions/14')
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_METHOD_NOT_ALLOWED)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(
            json_data.get('message'), ERROR_MESSAGES[STATUS_METHOD_NOT_ALLOWED]
        )

    def test_delete_question_failed_not_found(self):
        """
        Not found failed case of delete question test case.

        :return:
        """
        response = self.client().delete('/questions/-1000')
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_NOT_FOUND)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(
            json_data.get('message'), ERROR_MESSAGES[STATUS_NOT_FOUND]
        )

    def test_add_question_success(self):
        """
        Success case of add question test case.

        :return:
        """
        response = self.client().post('/questions', json=self.question)
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_CREATED)
        self.assertEqual(json_data.get('success'), True)
        self.assertTrue(json_data.get('id'))

    def test_add_question_failed_method_not_allowed(self):
        """
        Fail case of add question test case with method not allowed error.

        :return:
        """
        response = self.client().put('/questions', json={})
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_METHOD_NOT_ALLOWED)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(
            json_data.get('message'), ERROR_MESSAGES[STATUS_METHOD_NOT_ALLOWED]
        )

    def test_add_question_failed_bad_request(self):
        """
        Fail case of add question test case with bad request error.

        :return:
        """
        response = self.client().post('/questions', json={})
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_BAD_REQUEST)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(
            json_data.get('message'), ERROR_MESSAGES[STATUS_BAD_REQUEST]
        )

    def test_search_questions_success(self):
        """
        Success case of search questions api.

        :return:
        """
        data = {
            "searchTerm": "The"
        }
        response = self.client().post('/questions/filter', json=data)
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_OK)
        self.assertEqual(json_data.get('success'), True)
        self.assertTrue(len(json_data.get('questions')))
        self.assertTrue(json_data.get('total_questions'))

    def test_search_questions_failed(self):
        """
        Success case of search questions api with method not allowed error.

        :return:
        """
        response = self.client().get('/questions/filter', json={})
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_METHOD_NOT_ALLOWED)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(
            json_data.get('message'), ERROR_MESSAGES[STATUS_METHOD_NOT_ALLOWED]
        )

    def test_get_questions_by_category_success(self):
        """
        Success case for get questions by category.

        :return:
        """
        response = self.client().get('/categories/1/questions')
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_OK)
        self.assertEqual(json_data.get('success'), True)
        self.assertTrue(len(json_data.get('questions')))
        self.assertTrue(json_data.get('total_questions'))
        self.assertTrue(len(json_data.get('current_category')))

    def test_get_questions_by_category_failed_method_not_allowed(self):
        """
        Fail case for get questions by category with method not allowed error.

        :return:
        """
        response = self.client().post('/categories/1/questions')
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_METHOD_NOT_ALLOWED)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(
            json_data.get('message'), ERROR_MESSAGES[STATUS_METHOD_NOT_ALLOWED]
        )

    def test_get_questions_by_category_not_found(self):
        """
        Fail case for get questions by category with method not found.

        :return:
        """
        response = self.client().get('/categories/1000/questions')
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_NOT_FOUND)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(
            json_data.get('message'), ERROR_MESSAGES[STATUS_NOT_FOUND]
        )

    def test_play_quiz_success(self):
        """
        Success case for play quiz api.

        :return:
        """
        data = {
            "quiz_category": {
                "id": 1
            },
            "previous_questions": []
        }
        response = self.client().post('/quizzes', json=data)
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_OK)
        self.assertEqual(json_data.get('success'), True)
        self.assertTrue(len(json_data.get('question')))

    def test_play_quiz_failed_method_not_allowed(self):
        """
        Fail case for play quiz api with method not allowed error.

        :return:
        """
        response = self.client().get('/quizzes', json={})
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_METHOD_NOT_ALLOWED)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(
            json_data.get('message'), ERROR_MESSAGES[STATUS_METHOD_NOT_ALLOWED]
        )

    def test_play_quiz_failed_bad_request(self):
        """
        Fail case for play quiz api with method bad request.

        :return:
        """
        response = self.client().post('/quizzes', json={})
        json_data = response.get_json()
        self.assertEqual(response.status_code, STATUS_BAD_REQUEST)
        self.assertEqual(json_data.get('success'), False)
        self.assertEqual(
            json_data.get('message'), ERROR_MESSAGES[STATUS_BAD_REQUEST]
        )

    def tearDown(self):
        """
        Execute after reach test.

        :return:
        """
        pass


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
