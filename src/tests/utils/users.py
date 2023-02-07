import random
import string

from sqlalchemy.orm import Session

from app.users.schemas import UserCreate
from app.users.models import User

from app.users.services import AuthService


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def create_random_user(db: Session) -> User:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(username=email, email=email, password=password)
    user = AuthService(db).create_user(user_data=user_in)
    return user
