from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Boolean,
    CheckConstraint
)
from app.database import Base
from app.questions.models import Question


class Choice(Base):
    __tablename__ = 'choices'
    question_id = Column(
        Integer,
        ForeignKey(Question.question_id),
        primary_key=True
    )
    choice_index = Column(Integer, primary_key=True)
    content = Column(String(100), nullable=False)
    is_correct = Column(Boolean, nullable=False)

    __table_args__ = (
        CheckConstraint(
            choice_index >= 0, name='check_choice_index_positive'
        ), {}
    )
