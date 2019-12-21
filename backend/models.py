"""Module for model."""

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import Column, Integer, String

database_name = "trivia"

db = SQLAlchemy()


def get_database_path(db_name=database_name, is_postgres_user=False):
    """
    Get database path by given database_name.

    :param db_name:
    :param is_postgres_user:
    :return:
    """
    if is_postgres_user:
        return "postgres://{}/{}".format('localhost:5432', db_name)

    return "postgres://{}:{}@{}/{}".format('postgres', 'postgres', 'localhost:5432', db_name)


def setup_db(app, database_uri=get_database_path()):
    """
    Bind a flask application and a SQLAlchemy service.

    :param app:
    :param database_uri:
    :return:
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Question(db.Model):
    """Question."""

    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    category = Column(String)
    difficulty = Column(Integer)

    def __init__(self, question, answer, category, difficulty):
        """
        Init method.

        :param question:
        :param answer:
        :param category:
        :param difficulty:
        """
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty

    def insert(self):
        """
        Insert method.

        :return:
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def update():
        """
        Update method.

        :return:
        """
        db.session.commit()

    def delete(self):
        """
        Delete method.

        :return:
        """
        db.session.delete(self)
        db.session.commit()

    def format(self):
        """
        Format object.

        :return:
        """
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'difficulty': self.difficulty
        }


class Category(db.Model):
    """Category."""

    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String)

    def __init__(self, category_type):
        """
        Init method.

        :param category_type:
        """
        self.type = category_type

    def format(self):
        """
        Format method.

        :return:
        """
        return {
            'id': self.id,
            'type': self.type
        }
