from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Boolean,
    Enum
)
import enum
from app.database import Base
from app.quiz.models import Quiz


class QuestionTypes(str, enum.Enum):
    CHOICE = "C"
    MATCH_TEXT = "M"
    DESCRIPTION_TEXT = "D"


class Choice(Base):
    __tablename__ = 'choices'
    question_index = Column(Integer, ForeignKey('questions.question_index'))
    choice_index = Column(Integer, primary_key=True)
    content = Column(String(100), nullable=False)
    is_correct = Column(Boolean, nullable=False)


class Question(Base):
    __tablename__ = 'questions'
    question_index = Column(Integer, primary_key=True)
    quiz_id = Column(Integer, ForeignKey(Quiz.quiz_id))
    type = Column(
        Enum(
            *[question_type.value for question_type in QuestionTypes],
            name='question_types'
        ),
        nullable=False
    )
    content = Column(String(100), nullable=False)
    correct_answer = Column(String(100))
