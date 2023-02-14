import pytest
from jose import jwt
from sqlalchemy.orm import Session

from tests.utils.users import (
    random_email,
    random_lower_string,
    create_random_user
)

from app.settings import settings
from app.exceptions import (
    CredentialValidationException,
    AuthenticationException
)

from app.users import schemas

from app.users.services import AuthService


def test_create_user(db: Session):
    email = random_email()
    password = random_lower_string()
    user_in = schemas.UserCreate(
        username=email, email=email, password=password
    )
    user = AuthService(db).create_user(user_data=user_in)
    assert user.email == email
    assert hasattr(user, "password_hash")


def test_verify_password():
    password = random_lower_string()
    hashed_password = AuthService.hash_password(password)
    assert AuthService.verify_password(password, hashed_password) is True


def test_verify_password_fail():
    password1 = random_lower_string()
    password2 = random_lower_string()
    hashed_password = AuthService.hash_password(password1)
    assert AuthService.verify_password(password2, hashed_password) is False


@pytest.mark.parametrize(
    "jwt_field_name", ['iat', 'nbf', 'exp', 'sub', 'user']
)
def test_create_token(db: Session, jwt_field_name):
    user = create_random_user(db)
    token = AuthService.create_token(user=user)
    payload = jwt.decode(
        token.access_token,
        settings.jwt_secret,
        algorithms=[settings.jwt_algorithm],
    )
    assert jwt_field_name in payload


def test_verify_token(db: Session):
    user = create_random_user(db)
    token = AuthService.create_token(user=user)
    user_schema = schemas.User.from_orm(user)
    verified_user = AuthService.verify_token(token.access_token)
    assert verified_user == user_schema


def test_verify_token_credential_exception():
    token = random_lower_string()
    with pytest.raises(CredentialValidationException):
        AuthService.verify_token(token)


def test_authenticate_user(db: Session):
    email = random_email()
    password = random_lower_string()
    user_in = schemas.UserCreate(
        username=email, email=email, password=password
    )
    service = AuthService(db)
    user = service.create_user(user_data=user_in)
    token = service.authenticate_user(email, password)

    user_schema = schemas.User.from_orm(user)
    verified_user = AuthService.verify_token(token.access_token)
    assert verified_user == user_schema


def test_authenticate_user_wrong_username(db: Session):
    email = random_email()
    password = random_lower_string()
    user_in = schemas.UserCreate(
        username=email, email=email, password=password
    )
    service = AuthService(db)
    service.create_user(user_data=user_in)

    with pytest.raises(AuthenticationException):
        wrong_email = email + 'wrong'
        service.authenticate_user(wrong_email, password)


def test_authenticate_user_wrong_password(db: Session):
    email = random_email()
    password = random_lower_string()
    user_in = schemas.UserCreate(
        username=email, email=email, password=password
    )
    service = AuthService(db)
    service.create_user(user_data=user_in)

    with pytest.raises(AuthenticationException):
        wrong_password = password + 'wrong'
        service.authenticate_user(email, wrong_password)
