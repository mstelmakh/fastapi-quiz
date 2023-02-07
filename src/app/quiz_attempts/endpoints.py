from fastapi import APIRouter, status, Depends
from app.quiz_attempts.schemas import Attempt, AttemptCreate

from app.quiz_attempts.services import (
    AttemptService,
    attempt_user_verifier
)
from app.users.services import basic_verifier


router = APIRouter(
    prefix="/attempts",
    tags=["attempts"],
    dependencies=[Depends(basic_verifier)]
)


@router.get("/")
def list_all(service: AttemptService = Depends()) -> list[Attempt]:
    return service.get_many()


@router.get(
    "/{attempt_id}",
    dependencies=[Depends(attempt_user_verifier)]
)
async def get_by_id(
    attempt_id: int,
    service: AttemptService = Depends()
) -> Attempt:
    return service.get(attempt_id)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED
)
async def create(
    request: AttemptCreate,
    service: AttemptService = Depends()
) -> Attempt:
    return service.create(request)


@router.post(
    "/{attempt_id}/submit",
    dependencies=[Depends(attempt_user_verifier)]
)
async def submit(
    attempt_id: int,
    service: AttemptService = Depends()
) -> Attempt:
    return service.submit(attempt_id)
