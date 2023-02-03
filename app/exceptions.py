from fastapi import HTTPException, status


class UnauthorizedException(HTTPException):
    def __init__(self, detail='Unauthorized.') -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={'WWW-Authenticate': 'Bearer'}
        )


class CredentialValidationException(UnauthorizedException):
    def __init__(self) -> None:
        super().__init__(detail='Could not validate credentials.')


class AuthenticationException(UnauthorizedException):
    def __init__(self) -> None:
        super().__init__(detail='Incorrect username or password.')


class ForbiddenException(HTTPException):
    def __init__(self, detail='Forbidden.') -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            headers={'WWW-Authenticate': 'Bearer'},
        )


class NotAnOwnerException(ForbiddenException):
    def __init__(self) -> None:
        super().__init__(detail='Not an owner.')


class UniqueConstraintViolatedException(HTTPException):
    def __init__(self, column_name=None) -> None:
        column_message = " on column " + column_name if column_name else ""
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Unique constraint{column_message} violated.'
        )
