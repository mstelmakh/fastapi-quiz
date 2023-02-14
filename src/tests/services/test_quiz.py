import pytest
from fastapi import HTTPException

from sqlalchemy.orm import Session

from tests.utils.utils import random_lower_string
from tests.utils.users import create_random_user
from tests.utils.quiz import create_sample_quiz

from app.quiz import schemas

from app.quiz.services import QuizService


def test_create_quiz(db: Session):
    user = create_random_user(db)
    name = random_lower_string()
    description = random_lower_string()
    quiz_data = schemas.QuizCreate(
        name=name, description=description
    )
    quiz = QuizService(db, user).create(quiz_data)

    assert hasattr(quiz, "quiz_id")
    assert quiz.name == name
    assert quiz.description == description
    assert quiz.owner_id == user.user_id


def test_get_quiz(db: Session):
    user = create_random_user(db)
    quiz = create_sample_quiz(db, user)
    new_quiz = QuizService(db, user).get(quiz.quiz_id)
    assert quiz == new_quiz


def test_get_quiz_not_found(db: Session):
    user = create_random_user(db)
    quiz = create_sample_quiz(db, user)
    with pytest.raises(HTTPException):
        QuizService(db, user).get(quiz.quiz_id+1)


def test_get_many(db: Session):
    user = create_random_user(db)
    quiz1 = create_sample_quiz(db, user)
    quiz2 = create_sample_quiz(db, user)
    quiz_list = QuizService(db, user).get_many()
    assert len(quiz_list) == 2
    assert quiz1 in quiz_list and quiz2 in quiz_list


def test_update_quiz(db: Session):
    user = create_random_user(db)
    quiz = create_sample_quiz(db, user)
    new_name = quiz.name + "changed"
    new_description = quiz.description + "changed"
    quiz_data = schemas.QuizCreate(
        name=new_name, description=new_description
    )
    quiz = QuizService(db, user).update(
        quiz_id=quiz.quiz_id,
        quiz_data=quiz_data
    )
    assert quiz.name == new_name
    assert quiz.description == new_description


def test_delete_quiz(db: Session):
    user = create_random_user(db)
    quiz = create_sample_quiz(db, user)
    QuizService(db, user).delete(quiz.quiz_id)
    with pytest.raises(HTTPException):
        QuizService(db, user).get(quiz.quiz_id)
