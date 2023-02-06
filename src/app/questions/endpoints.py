from fastapi import APIRouter, status, Depends
from app.questions.schemas import (
    QuestionCreate,
    Question
)
from app.questions.services import QuestionService
from app.users.services import basic_verifier
from app.quiz.services import quiz_owner_verifier


router = APIRouter(
    prefix="/quiz/{quiz_id}/questions",
    tags=["questions"]
)


@router.get("/")
def list_all(
    service: QuestionService = Depends()
) -> list[Question]:
    return service.get_many()


@router.get(
    "/{question_index}",
    dependencies=[Depends(basic_verifier)]
)
async def get_by_id(
    question_index: int,
    service: QuestionService = Depends()
) -> Question:
    return service.get(question_index)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(basic_verifier), Depends(quiz_owner_verifier)]
)
async def create(
    request: QuestionCreate,
    service: QuestionService = Depends()
) -> Question:
    return service.create(request)


@router.put(
    "/{question_index}",
    dependencies=[Depends(basic_verifier), Depends(quiz_owner_verifier)]
)
async def update(
    question_index: int,
    request: QuestionCreate,
    service: QuestionService = Depends()
) -> Question:
    return service.update(question_index, request)


@router.delete(
    "/{question_index}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(basic_verifier), Depends(quiz_owner_verifier)]
)
async def delete(
    question_index: int,
    service: QuestionService = Depends()
) -> None:
    return service.delete(question_index)
