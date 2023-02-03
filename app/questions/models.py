from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Enum,
    CheckConstraint
)
import enum
from app.database import Base
from app.quiz.models import Quiz


class QuestionTypes(str, enum.Enum):
    CHOICE = "C"
    MATCH_TEXT = "M"
    DESCRIPTION_TEXT = "D"


class Question(Base):
    __tablename__ = 'questions'
    question_id = Column(Integer, primary_key=True)
    quiz_id = Column(Integer, ForeignKey(Quiz.quiz_id))
    question_index = Column(Integer)
    type = Column(
        Enum(
            *[question_type.value for question_type in QuestionTypes],
            name='question_types'
        ),
        nullable=False
    )
    content = Column(String(100), nullable=False)
    correct_answer = Column(String(100))

    __table_args__ = (
        CheckConstraint(
            question_index >= 0, name='check_question_index_positive'
        ), {}
    )
