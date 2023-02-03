from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    DateTime,
    String
)
from app.database import Base
from app.questions.models import Question


class QuizAttempt(Base):
    __tablename__ = 'quiz_attempts'
    attempt_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    quiz_id = Column(Integer, ForeignKey('quiz.quiz_id'))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)


class Answer(Base):
    __tablename__ = 'answers'
    answer_id = Column(Integer, primary_key=True)
    attempt_id = Column(Integer, ForeignKey(QuizAttempt.attempt_id))
    question_id = Column(Integer, ForeignKey(Question.question_index))
    text_answer = Column(String(100), nullable=True)
    choice_index = Column(
        Integer,
        ForeignKey('choices.choice_index'),
        nullable=True
    )
