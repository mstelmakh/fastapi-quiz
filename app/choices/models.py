from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Boolean
)
from app.database import Base


class Choice(Base):
    __tablename__ = 'choices'
    quiz_id = Column(Integer, ForeignKey('quiz.quiz_id'))
    question_index = Column(Integer, ForeignKey('questions.question_index'))
    choice_index = Column(Integer, primary_key=True)
    content = Column(String(100), nullable=False)
    is_correct = Column(Boolean, nullable=False)
