from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String
)
from sqlalchemy.orm import relationship
from app.database import Base


class Quiz(Base):
    __tablename__ = 'quiz'
    quiz_id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('users.user_id'))
    name = Column(String(100), nullable=False)
    description = Column(String(400))

    questions = relationship("Question", back_populates="quiz")
    quiz_attempts = relationship("QuizAttempt", back_populates="quiz")
    owner = relationship("User", back_populates="owned_quizzes")
