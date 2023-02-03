from datetime import (
    datetime,
    timedelta,
)

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import (
    JWTError,
    jwt,
)
from passlib.hash import bcrypt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.exceptions import (
    UnauthorizedException,
    CredentialValidationException,
    AuthenticationException
)
from app.users import (
    models,
    schemas
)
from app.database import get_session
from app.settings import settings


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/auth/sign-in/', auto_error=False
)


def get_current_user(token: str = Depends(oauth2_scheme)) -> schemas.User:
    return AuthService.get_current_user(token)


def basic_verifier(
    current_user: schemas.User | None = Depends(get_current_user)
):
    if not current_user:
        raise UnauthorizedException()


class AuthService:
    @classmethod
    def verify_password(
        cls, plain_password: str, hashed_password: str
    ) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def verify_token(cls, token: str) -> schemas.User:
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm],
            )
        except JWTError:
            raise CredentialValidationException() from None

        user_data = payload.get('user')

        try:
            user = schemas.User.parse_obj(user_data)
        except ValidationError:
            raise CredentialValidationException() from None

        return user

    @classmethod
    def create_token(cls, user: models.User) -> schemas.Token:
        user_data = schemas.User.from_orm(user)
        now = datetime.utcnow()
        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(seconds=settings.jwt_expires_s),
            'sub': str(user_data.user_id),
            'user': user_data.dict(),
        }
        token = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm,
        )
        return schemas.Token(access_token=token)

    @classmethod
    def get_current_user(cls, token: str | None = None) -> schemas.User:
        if not token:
            return None
        return cls.verify_token(token)

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def register_new_user(
        self,
        user_data: schemas.UserCreate,
    ) -> schemas.Token:
        user = models.User(
            email=user_data.email,
            username=user_data.username,
            password_hash=self.hash_password(user_data.password),
        )
        self.session.add(user)
        self.session.commit()
        return self.create_token(user)

    def authenticate_user(
        self,
        username: str,
        password: str,
    ) -> schemas.Token:
        user = (
            self.session
            .query(models.User)
            .filter(models.User.username == username)
            .first()
        )

        if not user:
            raise AuthenticationException()

        if not self.verify_password(password, user.password_hash):
            raise AuthenticationException()

        return self.create_token(user)
