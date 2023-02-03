from fastapi import APIRouter, status, Depends
from app.choices.schemas import (
    ChoiceCreate,
    Choice
)
from app.choices.services import ChoiceService
from app.users.services import basic_verifier
from app.quiz.services import quiz_owner_verifier


router = APIRouter(
    prefix="/quiz/{quiz_id}/questions/{question_index}/choices",
    tags=["choices"]
)


@router.get("/")
def list_all(
    service: ChoiceService = Depends()
) -> list[Choice]:
    return service.get_many()


@router.get(
    "/{choice_index}",
    dependencies=[Depends(basic_verifier)]
)
async def get_by_id(
    choice_index: int,
    service: ChoiceService = Depends()
) -> Choice:
    return service.get(choice_index)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(basic_verifier), Depends(quiz_owner_verifier)]
)
async def create(
    request: ChoiceCreate,
    service: ChoiceService = Depends()
) -> Choice:
    return service.create(request)


@router.put(
    "/{choice_index}",
    dependencies=[Depends(basic_verifier), Depends(quiz_owner_verifier)]
)
async def update(
    choice_index: int,
    request: ChoiceCreate,
    service: ChoiceService = Depends()
) -> Choice:
    return service.update(choice_index, request)


@router.delete(
    "/{choice_index}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(basic_verifier), Depends(quiz_owner_verifier)]
)
async def delete(
    choice_index: int,
    service: ChoiceService = Depends()
) -> None:
    return service.delete(choice_index)
