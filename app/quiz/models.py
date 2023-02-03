from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String
)
from app.database import Base
from app.users.models import User


class Quiz(Base):
    __tablename__ = 'quiz'
    quiz_id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey(User.user_id))
    name = Column(String(100), nullable=False)
    description = Column(String(400))
