from pydantic import BaseModel
from app.questions.models import QuestionTypes


class BaseChoice(BaseModel):
    question_index: int
    choice_index: int
    content: str


class ChoiceCreate(BaseChoice):
    is_correct: bool


class Choice(BaseChoice):
    pass

    class Config:
        orm_mode = True


class BaseQuestion(BaseModel):
    question_index: int
    quiz_id: int
    type: QuestionTypes
    content: str


class QuestionCreate(BaseQuestion):
    correct_answer: str


class Question(BaseQuestion):
    pass

    class Config:
        orm_mode = True
