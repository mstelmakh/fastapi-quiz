from pydantic import BaseModel
from app.questions.models import QuestionTypes


class BaseQuestion(BaseModel):
    question_index: int
    type: QuestionTypes
    content: str


class QuestionCreate(BaseQuestion):
    correct_answer: str


class Question(BaseQuestion):
    quiz_id: int

    class Config:
        orm_mode = True
