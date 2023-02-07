from pydantic import BaseModel
from datetime import datetime


class BaseAttempt(BaseModel):
    quiz_id: int


class AttemptCreate(BaseAttempt):
    pass


class Attempt(BaseAttempt):
    attempt_id: int
    user_id: int
    start_time: datetime
    end_time: datetime | None

    class Config:
        orm_mode = True
