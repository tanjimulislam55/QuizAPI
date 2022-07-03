from typing import Optional
from sqlalchemy import select, or_

from schemas.quizes import QuestionCreate, AnswerCreate, OptionCreate
from models import Question, Option, QuestionAnswer
from .base import CRUDBase
from utils.db import database


class CRUDQuestion(CRUDBase[Question, QuestionCreate, None]):
    async def get_many(
        self, skip: int, limit: int, type_: str, category: str, quiz_amount: int
    ) -> Optional[Question]:
        query = (
            select(Question)
            .where(
                or_(
                    Question.type_ == type_,
                    Question.category == category,
                    Question.quiz_amount == quiz_amount,
                )
            )
            .join(Option)
            .where(Question.id == Option.question_id)
            .offset(skip)
            .limit(limit)
        )
        return await database.fetch_all(query)


class CRUDOption(CRUDBase[Option, OptionCreate, None]):
    pass


class CRUDAnswer(CRUDBase[QuestionAnswer, QuestionAnswer, None]):
    pass


question = CRUDQuestion(Question)
option = CRUDOption(Option)
answer = CRUDAnswer(QuestionAnswer)
