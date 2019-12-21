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


def get_all_categories():
    """
    Get all categories.

    :return:
    """
    categories = {}
    for category in Category.query.all():
        categories[category.id] = category.type

    return categories


def get_category_by_id(category_id):
    """
    Return category by given category_id id.

    :param category_id:
    :return:
    """
    return Category.query.get(category_id)


def get_all_questions(query=None, category_id=None):
    """
    Return list of all questions.

    :param query:
    :param category_id:
    :return:
    """
    if query:
        questions = Question.query.filter(
            Question.question.ilike(f'%{query}%')
        )
    elif category_id:
        questions = Question.query.filter_by(category=category_id)
    else:
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


def get_question_by_id(question_id):
    """
    Return question by given question id.

    :param question_id:
    :return:
    """
    return Question.query.get(question_id)


def add_new_question(question):
    """
    Add new question to db.

    :param question:
    :return:
    """
    instance = Question(**question)
    instance.insert()
    return instance
