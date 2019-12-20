"""Module for app."""

import random

from flask import Flask, abort, jsonify, request

from flask_cors import CORS

from flaskr.constants import (
    ERROR_MESSAGES, STATUS_BAD_REQUEST, STATUS_CREATED, STATUS_FORBIDDEN, STATUS_INTERNAL_SERVER_ERROR,
    STATUS_METHOD_NOT_ALLOWED, STATUS_NOT_FOUND, STATUS_NO_CONTENT, STATUS_UNAUTHORIZED, STATUS_UNPROCESSABLE_ENTITY
)
from flaskr.utils import (
    add_new_question, get_all_categories, get_all_questions,
    get_category_by_id, get_question_by_id, get_questions_by_page
)

from models import setup_db


def create_app(test_config=None):
    """
    Create and configure the app.

    :param test_config:
    :return:
    """
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r"*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/categories')
    def get_categories():
        """
        Return the categories with id and type.

        :return:
        """
        try:
            result = {
                "success": True,
                "categories": get_all_categories()
            }
            return jsonify(result)

        except Exception as exp:
            abort(exp.code)

    @app.route('/questions')
    def get_questions():
        """
        Get questions by given page number.

        :return:
        """
        try:
            page = request.args.get('page', 1, type=int)
            questions = get_questions_by_page(page)

            if len(questions) == 0:
                abort(STATUS_NOT_FOUND)

            return jsonify({
                'success': True,
                'current_category': None,
                'categories': get_all_categories(),
                'questions': questions,
                'total_questions': len(get_all_questions())
            })

        except Exception as exp:
            abort(exp.code)

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        """
        Delete question by given question id.

        :param question_id:
        :return:
        """
        try:
            question = get_question_by_id(question_id)
            if not question:
                abort(STATUS_NOT_FOUND)

            question.delete()
            return jsonify({
                'success': True
            }), STATUS_NO_CONTENT

        except Exception as exp:
            abort(exp.code)

    @app.route('/questions', methods=['POST'])
    def add_question():
        """
        Add question to database.

        :return:
        """
        try:
            question = request.get_json()

            if not question:
                abort(STATUS_BAD_REQUEST)

            add_new_question(question)
            return jsonify({
                'success': True,
            }), STATUS_CREATED

        except Exception as exp:
            abort(exp.code)

    @app.route('/questions/filter', methods=['POST'])
    def search_questions():
        """
        Return the list of questions filtered by given search.

        :return:
        """
        try:
            request_data = request.get_json()
            questions = get_all_questions(query=request_data.get('searchTerm'))
            return jsonify({
                'success': True,
                'questions': questions,
                'total_questions': len(questions),
            })

        except Exception as exp:
            abort(exp.code)

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        """
        Get questions by category.

        :param category_id:
        :return:
        """
        try:
            category = get_category_by_id(category_id)

            if category is None:
                abort(STATUS_NOT_FOUND)

            questions = get_all_questions(category_id=category_id)
            return jsonify({
                "success": True,
                "questions": questions,
                "total_questions": len(questions),
                "current_category": category.format(),
            })

        except Exception as exp:
            abort(exp.code)

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        """
        Play quiz route to get questions for quizzes.

        :return:
        """
        try:
            request_data = request.get_json()
            previous_questions = request_data.get('previous_questions', [])
            quiz_category = request_data.get('quiz_category')

            if not quiz_category:
                abort(STATUS_BAD_REQUEST)

            category_id = quiz_category.get('id', 0)
            questions = get_all_questions() if category_id == 0 else get_all_questions(category_id=category_id)

            filtered_questions = list(filter(lambda question: question.get('id') not in previous_questions, questions))

            random_question = random.choice(filtered_questions) if filtered_questions else None

            return jsonify({
                'question': random_question,
                'success': True
            })

        except Exception as exp:
            abort(exp.code)

    @app.errorhandler(STATUS_BAD_REQUEST)
    def bad_request(error):
        """
        Error handler for bad request with status code 400.

        :param: error
        :return:
        """
        return jsonify({
            'success': False,
            'error': STATUS_BAD_REQUEST,
            'message': ERROR_MESSAGES[STATUS_BAD_REQUEST]
        }), STATUS_BAD_REQUEST

    @app.errorhandler(STATUS_UNAUTHORIZED)
    def unauthorized(error):
        """
        Error handler for unauthorized with status code 401.

        :param: error
        :return:
        """
        return jsonify({
            'success': False,
            'error': STATUS_UNAUTHORIZED,
            'message': ERROR_MESSAGES[STATUS_UNAUTHORIZED]
        }), STATUS_UNAUTHORIZED

    @app.errorhandler(STATUS_FORBIDDEN)
    def forbidden(error):
        """
        Error handler for forbidden with status code 403.

        :param: error
        :return:
        """
        return jsonify({
            'success': False,
            'error': STATUS_FORBIDDEN,
            'message': ERROR_MESSAGES[STATUS_FORBIDDEN]
        }), STATUS_FORBIDDEN

    @app.errorhandler(STATUS_NOT_FOUND)
    def not_found(error):
        """
        Error handler for not found with status code 404.

        :param: error
        :return:
        """
        return jsonify({
            'success': False,
            'error': STATUS_NOT_FOUND,
            'message': ERROR_MESSAGES[STATUS_NOT_FOUND]
        }), STATUS_NOT_FOUND

    @app.errorhandler(STATUS_METHOD_NOT_ALLOWED)
    def method_not_allowed(error):
        """
        Error handler for method not allowed with status code 405.

        :param: error
        :return:
        """
        return jsonify({
            'success': False,
            'error': STATUS_METHOD_NOT_ALLOWED,
            'message': ERROR_MESSAGES[STATUS_METHOD_NOT_ALLOWED]
        }), STATUS_METHOD_NOT_ALLOWED

    @app.errorhandler(STATUS_UNPROCESSABLE_ENTITY)
    def unprocessable_entity(error):
        """
        Error handler for unprocessable entity with status code 422.

        :param: error
        :return:
        """
        return jsonify({
            'success': False,
            'error': STATUS_UNPROCESSABLE_ENTITY,
            'message': ERROR_MESSAGES[STATUS_UNPROCESSABLE_ENTITY]
        }), STATUS_UNPROCESSABLE_ENTITY

    @app.errorhandler(STATUS_INTERNAL_SERVER_ERROR)
    def internal_server_error(error):
        """
        Error handler for internal server error with status code 500.

        :param: error
        :return:
        """
        return jsonify({
            'success': False,
            'error': STATUS_INTERNAL_SERVER_ERROR,
            'message': ERROR_MESSAGES[STATUS_INTERNAL_SERVER_ERROR]
        }), STATUS_INTERNAL_SERVER_ERROR

    return app
