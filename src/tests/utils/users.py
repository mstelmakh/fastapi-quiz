
from sqlalchemy.orm import Session

from app.users.schemas import UserCreate
from app.users.models import User

from app.users.services import AuthService

from tests.utils.utils import random_lower_string


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def create_random_user(db: Session) -> User:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(username=email, email=email, password=password)
    user = AuthService(db).create_user(user_data=user_in)
    return user


def register_random_user(db: Session) -> User:
    user = create_random_user()
    return AuthService(db).create_token(user)
