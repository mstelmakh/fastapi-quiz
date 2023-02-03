from sqlalchemy import (
    Column,
    String,
    Integer,
)
from app.database import Base


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    password_hash = Column(String)
