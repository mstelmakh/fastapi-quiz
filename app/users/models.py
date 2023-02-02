from sqlalchemy import (
    Column,
    Integer,
)
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)

    owned_quizzes = relationship("Quiz", back_populates="owner")
    quiz_attempts = relationship("QuizAttempt", back_populates="user")
