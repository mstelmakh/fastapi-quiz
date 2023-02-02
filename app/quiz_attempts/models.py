from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    DateTime,
    String
)
from sqlalchemy.orm import relationship
from app.database import Base


class QuizAttempt(Base):
    __tablename__ = 'quiz_attempts'
    attempt_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    quiz_id = Column(Integer, ForeignKey('quiz.quiz_id'))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)

    quiz = relationship("Quiz", back_populates="quiz_attempts")
    user = relationship("User", back_populates="quiz_attempts")
    answers = relationship("Answer", back_populates="attempt")


class Answer(Base):
    __tablename__ = 'answers'
    answer_id = Column(Integer, primary_key=True)
    attempt_id = Column(Integer, ForeignKey('quiz_attempts.attempt_id'))
    question_id = Column(Integer, ForeignKey('questions.question_index'))
    text_answer = Column(String(100), nullable=True)
    choice_index = Column(
        Integer,
        ForeignKey('choices.choice_index'),
        nullable=True
    )

    attempt = relationship("quiz_attempts", back_populates="answers")
    question = relationship("questions", back_populates="answers")
    choice = relationship("choices", back_populates="answers")
