from pydantic import BaseModel


class BaseChoice(BaseModel):
    choice_index: int
    content: str


class ChoiceCreate(BaseChoice):
    is_correct: bool


class Choice(BaseChoice):
    question_id: int

    class Config:
        orm_mode = True
