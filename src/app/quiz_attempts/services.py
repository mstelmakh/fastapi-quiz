from datetime import datetime
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.exceptions import NotAnOwnerException
from app.database import get_session

from app.quiz_attempts import schemas
from app.quiz_attempts import models

from app.users.schemas import User
from app.users.services import get_current_user


class AttemptService:
    def __init__(
        self,
        db: Session = Depends(get_session),
        current_user: User = Depends(get_current_user)
    ):
        self.db = db
        self.current_user = current_user

    def get(self, attempt_id: int) -> schemas.Attempt:
        return self._get(attempt_id)

    def _get(self, attempt_id: int) -> models.Attempt:
        attempt = (
            self.db
            .query(models.Attempt)
            .filter_by(
                attempt_id=attempt_id
            )
            .first()
        )
        if not attempt:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return attempt

    def get_many(self) -> list[models.Attempt]:
        attemptes = (
            self.db
            .query(models.Attempt)
            .order_by(
                models.Attempt.attempt_id.desc(),
            )
            .all()
        )
        return attemptes

    def create(
        self,
        attempt_data: schemas.AttemptCreate
    ) -> models.Attempt:
        attempt = models.Attempt(
            **attempt_data.dict(),
            start_time=datetime.now(),
            user_id=self.current_user.user_id
        )
        self.db.add(attempt)
        self.db.commit()
        return attempt

    def submit(
        self,
        attempt_id: int
    ) -> models.Attempt:
        attempt = self._get(attempt_id)
        attempt.end_time = datetime.now()
        self.db.commit()
        return attempt

    def delete(
        self,
        attempt_id: int,
    ):
        attempt = self._get(attempt_id)
        self.db.delete(attempt)
        self.db.commit()


def attempt_user_verifier(
    attempt_id: int,
    current_user: User = Depends(get_current_user),
    service: AttemptService = Depends()
):
    if not service.get(attempt_id).user_id == current_user.user_id:
        raise NotAnOwnerException()
