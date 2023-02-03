from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.exceptions import UniqueConstraintViolatedException

from app.database import get_session

from app.choices import schemas
from app.choices import models

from app.users.schemas import User
from app.users.services import get_current_user


class ChoiceService:
    def __init__(
        self,
        quiz_id: int,
        question_index: int,
        db: Session = Depends(get_session),
        current_user: User = Depends(get_current_user)
    ):
        self.db = db
        self.current_user = current_user
        self.quiz_id = quiz_id
        self.question_index = question_index

    def get(self, choice_index: int) -> schemas.Choice:
        return self._get(choice_index)

    def _get(self, choice_index: int) -> models.Choice:
        choice = (
            self.db
            .query(models.Choice)
            .filter(
                models.Choice.choice_index == choice_index,
                models.Choice.quiz_id == self.quiz_id,
                models.Choice.question_index == self.question_index,
            )
            .first()
        )
        if not choice:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return choice

    def get_many(self) -> list[models.Choice]:
        choices = (
            self.db
            .query(models.Choice)
            .filter(
                models.Choice.quiz_id == self.quiz_id,
                models.Choice.question_index == self.question_index
            )
            .order_by(
                models.Choice.choice_index.desc(),
            )
            .all()
        )
        return choices

    def create(
        self,
        choice_data: schemas.ChoiceCreate
    ) -> models.Choice:
        choice = models.Choice(
            **choice_data.dict(),
            quiz_id=self.quiz_id,
            question_index=self.question_index
        )
        try:
            self.db.add(choice)
            self.db.commit()
        except IntegrityError:
            raise UniqueConstraintViolatedException(
                column_name="choice_index"
            )
        return choice

    def update(
        self,
        choice_index: int,
        choice_data: schemas.ChoiceCreate,
    ) -> models.Choice:
        choice = self._get(choice_index)
        for field, value in choice_data:
            setattr(choice, field, value)
        try:
            self.db.commit()
        except IntegrityError:
            raise UniqueConstraintViolatedException(
                column_name="choice_index"
            )
        return choice

    def delete(
        self,
        choice_index: int,
    ):
        choice = self._get(choice_index)
        self.db.delete(choice)
        self.db.commit()
