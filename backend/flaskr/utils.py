"""Utils module for flaskr app."""

from flaskr.constants import QUESTIONS_PER_PAGE

from models import Category, Question


def get_page_range(page):
    """
    Get page range.

    :param page:
    :return: start, end
    """
    page_index = page - 1
    start = page_index * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    return start, end


def get_all_questions():
    """
    Return list of all questions.

    :return:
    """
    questions = Question.query.order_by(Question.id).all()
    serialized_data = [question.format() for question in questions]
    return serialized_data


def get_questions_by_page(page):
    """
    Return list of questions by given page.

    :param page:
    :return:
    """
    start, end = get_page_range(page)
    questions = get_all_questions()
    return questions[start:end]


def get_all_categories():
    """
    Get all categories.

    :return:
    """
    categories = {}
    for category in Category.query.all():
        categories[category.id] = category.type

    return categories
