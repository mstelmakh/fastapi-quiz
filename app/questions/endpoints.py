from fastapi import APIRouter, status
from app.questions.schemas import (
    QuestionCreate,
    Question,
    ChoiceCreate,
    Choice
)


router = APIRouter(
    prefix="/quiz/{quiz_id}/questions",
    tags=["questions"]
)


@router.get("/")
def list_all_questions(quiz_id: int) -> list[Question]:
    pass


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED
)
async def create_question(request: QuestionCreate) -> Question:
    pass


@router.put("/{question_id}")
async def update_question(
    quiz_id: int,
    question_id: int,
    request: QuestionCreate
) -> Question:
    pass


@router.delete(
    "/{question_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_question(
    quiz_id: int,
    question_id: int
):
    pass


@router.get("/{question_id}/choices/")
def list_all_choices(quiz_id: int, question_id: int) -> list[Choice]:
    pass


@router.post(
    "/{question_id}/choices/",
    status_code=status.HTTP_201_CREATED
)
async def create_choice(
    quiz_id: int,
    question_id: int,
    request: ChoiceCreate
) -> Choice:
    pass


@router.put("/{question_id}/choices/{choice_id}")
async def update_choice(
    quiz_id: int,
    question_id: int,
    choice_id: int,
    request: ChoiceCreate
) -> Choice:
    pass


@router.delete(
    "/{question_id}/choices/{choice_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_choice(
    quiz_id: int,
    question_id: int,
    choice_id: int
):
    pass
