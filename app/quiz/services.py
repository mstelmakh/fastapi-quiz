from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_session

from app.quiz import schemas
from app.quiz import models

from app.users.schemas import User
from app.users.services import get_current_user


class QuizService:
    def __init__(
        self,
        db: Session = Depends(get_session),
        current_user: User = Depends(get_current_user)
    ):
        self.db = db
        self.current_user = current_user

    def get(self, quiz_id: int) -> schemas.Quiz:
        return self._get(quiz_id)

    def _get(self, quiz_id: int) -> models.Quiz:
        quiz = (
            self.db
            .query(models.Quiz)
            .filter(
                models.Quiz.quiz_id == quiz_id
            )
            .first()
        )
        if not quiz:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return quiz

    def get_many(self) -> list[models.Quiz]:
        quizes = (
            self.db
            .query(models.Quiz)
            .order_by(
                models.Quiz.quiz_id.desc(),
            )
            .all()
        )
        return quizes

    def create(
        self,
        quiz_data: schemas.QuizCreate
    ) -> models.Quiz:
        quiz = models.Quiz(
            **quiz_data.dict(),
            owner_id=self.current_user.user_id
        )
        self.db.add(quiz)
        self.db.commit()
        return quiz

    def update(
        self,
        quiz_id: int,
        quiz_data: schemas.QuizCreate,
    ) -> models.Quiz:
        quiz = self._get(quiz_id)
        for field, value in quiz_data:
            setattr(quiz, field, value)
        self.db.commit()
        return quiz

    def delete(
        self,
        quiz_id: int,
    ):
        quiz = self._get(quiz_id)
        self.db.delete(quiz)
        self.db.commit()


def quiz_owner_verifier(
    quiz_id: int,
    current_user: User = Depends(get_current_user),
    quiz_service: QuizService = Depends()
):
    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Not an owner of this quiz',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    if not quiz_service.get(quiz_id).owner_id == current_user.user_id:
        raise exception
