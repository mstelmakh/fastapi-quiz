from fastapi import APIRouter, status, Depends
from app.quiz.schemas import Quiz, QuizCreate

from app.quiz.services import quiz_owner_verifier, QuizService
from app.users.services import basic_verifier


router = APIRouter(
    prefix="/quiz",
    tags=["quiz"]
)


@router.get("/")
def list_all(service: QuizService = Depends()) -> list[Quiz]:
    return service.get_many()


@router.get(
    "/{quiz_id}",
    response_model=Quiz,
    dependencies=[Depends(basic_verifier), Depends(quiz_owner_verifier)]
)
async def get_by_id(
    quiz_id: int,
    service: QuizService = Depends()
):
    return service.get(quiz_id)


@router.post(
    "/",
    response_model=Quiz,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(basic_verifier)]
)
async def create(
    request: QuizCreate,
    service: QuizService = Depends()
):
    return service.create(request)


@router.put(
    "/{quiz_id}",
    response_model=Quiz,
    dependencies=[Depends(basic_verifier), Depends(quiz_owner_verifier)]
)
async def update(
    quiz_id: int,
    request: QuizCreate,
    service: QuizService = Depends()
):
    return service.update(quiz_id, request)


@router.delete(
    "/{quiz_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(basic_verifier), Depends(quiz_owner_verifier)]
)
async def delete(
    quiz_id: int,
    service: QuizService = Depends()
):
    return service.delete(quiz_id)
