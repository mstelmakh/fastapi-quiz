from pydantic import BaseModel


class BaseQuiz(BaseModel):
    name: str
    description: str


class QuizCreate(BaseQuiz):
    pass


class Quiz(BaseQuiz):
    quiz_id: int
    owner_id: int

    class Config:
        orm_mode = True
