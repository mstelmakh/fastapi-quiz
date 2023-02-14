from sqlalchemy.orm import Session

from app.users.models import User
from app.quiz.models import Quiz
from app.quiz import schemas

from tests.utils.utils import random_lower_string

from app.quiz.services import QuizService


def create_sample_quiz(db: Session, user: User) -> Quiz:
    name = random_lower_string()
    description = random_lower_string()
    quiz_data = schemas.QuizCreate(
        name=name, description=description
    )
    quiz = QuizService(db, user).create(quiz_data)
    return quiz
