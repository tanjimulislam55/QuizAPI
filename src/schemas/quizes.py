from pydantic import BaseModel
from typing import Optional, List


class OptionCreate(BaseModel):
    option: str
    is_correct_option: bool


class OptionInDB(OptionCreate):
    question_id: int


class QuestionInDB(BaseModel):
    question: str
    quiz_amount: int
    category: str
    type_: str


class QuestionCreate(QuestionInDB):
    options: List[OptionCreate]


class AnswerCreate(BaseModel):
    is_right: bool
    user_id: int
    question_id: int
    option_id: int


class QuestionOut(QuestionCreate):
    id: int

    class Config:
        orm_mode = True


class OptionOut(BaseModel):
    id: int
    option: str

    class Config:
        orm_mode = True


class OptionAnswerOut(AnswerCreate):
    id: int

    class Config:
        orm_mode = True
