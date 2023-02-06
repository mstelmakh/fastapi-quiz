from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    DateTime,
    String
)
from app.database import Base
from app.choices.models import Choice


class QuizAttempt(Base):
    __tablename__ = 'quiz_attempts'
    attempt_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    quiz_id = Column(Integer, ForeignKey('quiz.quiz_id'))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)


class Answer(Base):
    __tablename__ = 'answers'
    attempt_id = Column(
        Integer,
        ForeignKey(QuizAttempt.attempt_id),
        primary_key=True
    )
    question_id = Column(
        Integer,
        ForeignKey(Choice.question_id),
        primary_key=True
    )
    text_answer = Column(String(200))


class ChosenAnswer(Base):
    __tablename__ = 'chosen_answers'
    attempt_id = Column(
        Integer,
        ForeignKey(QuizAttempt.attempt_id),
        primary_key=True
    )
    question_id = Column(
        Integer,
        ForeignKey(Choice.question_id),
        primary_key=True
    )
    choice_index = Column(
        Integer,
        ForeignKey(Choice.choice_index),
        primary_key=True
    )
