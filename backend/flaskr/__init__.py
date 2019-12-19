"""Module for app."""

from flask import Flask, abort, jsonify

from flask_cors import CORS

from flaskr.constants import (
    ERROR_MESSAGES,
    STATUS_BAD_REQUEST, STATUS_FORBIDDEN, STATUS_METHOD_NOT_ALLOWED,
    STATUS_NOT_FOUND, STATUS_UNAUTHORIZED, STATUS_UNPROCESSABLE_ENTITY
)

from models import Category, setup_db

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    """
    Create and configure the app.

    :param test_config:
    :return:
    """
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r"*": {"origins": "*"}})

    # after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')
        return response

    '''
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    '''

    @app.route("/categories")
    def get_categories():
        """
        Return the list of categories with id and type.

        :return:
        """
        try:
            categories = Category.query.all()
            serialized_data = {}
            for category in categories:
                serialized_data[category.id] = category.type

            result = {
                "success": True,
                "categories": serialized_data
            }
            return jsonify(result)

        except Exception:
            abort(STATUS_UNPROCESSABLE_ENTITY)

    '''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''

    '''
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''

    '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    '''

    '''
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''

    '''
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''

    '''
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''

    @app.errorhandler(STATUS_BAD_REQUEST)
    def bad_request(error):
        """
        Error handler for bad request with status code 400.

        :param error:
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

        :param error:
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

        :param error:
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

        :param error:
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

        :param error:
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

        :param error:
        :return:
        """
        return jsonify({
            'success': False,
            'error': STATUS_UNPROCESSABLE_ENTITY,
            'message': ERROR_MESSAGES[STATUS_UNPROCESSABLE_ENTITY]
        }), STATUS_UNPROCESSABLE_ENTITY

    return app
