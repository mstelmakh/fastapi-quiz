from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.exceptions import UniqueConstraintViolatedException

from app.database import get_session

from app.questions import schemas
from app.questions import models

from app.users.schemas import User
from app.users.services import get_current_user


class QuestionService:
    def __init__(
        self,
        quiz_id: int,
        db: Session = Depends(get_session),
        current_user: User = Depends(get_current_user)
    ):
        self.db = db
        self.current_user = current_user
        self.quiz_id = quiz_id

    def get(self, question_index: int) -> schemas.Question:
        return self._get(question_index)

    def _get(self, question_index: int) -> models.Question:
        question = (
            self.db
            .query(models.Question)
            .filter(
                models.Question.question_index == question_index,
                models.Question.quiz_id == self.quiz_id
            )
            .first()
        )
        if not question:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return question

    def get_many(self) -> list[models.Question]:
        questions = (
            self.db
            .query(models.Question)
            .filter(
                models.Question.quiz_id == self.quiz_id
            )
            .order_by(
                models.Question.question_index.desc(),
            )
            .all()
        )
        return questions

    def create(
        self,
        question_data: schemas.QuestionCreate
    ) -> models.Question:
        question = models.Question(
            **question_data.dict(),
            quiz_id=self.quiz_id
        )
        try:
            self.db.add(question)
            self.db.commit()
        except IntegrityError:
            raise UniqueConstraintViolatedException(
                column_name="question_index"
            )
        return question

    def update(
        self,
        question_index: int,
        question_data: schemas.QuestionCreate,
    ) -> models.Question:
        question = self._get(question_index)
        for field, value in question_data:
            setattr(question, field, value)
        try:
            self.db.commit()
        except IntegrityError:
            raise UniqueConstraintViolatedException(
                column_name="question_index"
            )
        return question

    def delete(
        self,
        question_index: int,
    ):
        question = self._get(question_index)
        self.db.delete(question)
        self.db.commit()
