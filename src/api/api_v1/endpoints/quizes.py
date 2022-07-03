from typing import List, Optional
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from schemas.quizes import (
    QuestionCreate,
    QuestionInDB,
    QuestionOut,
    OptionInDB,
    OptionOut,
    AnswerCreate,
    OptionAnswerOut,
)
from models import User
from ...dependencies import get_current_user, get_current_active_superuser
from crud.quizes import question, option, answer

router = APIRouter()


@router.get(
    "/",
    # response_model=List[QuestionOut],
    status_code=status.HTTP_200_OK,
)
async def get_multiple_questions(
    skip: int = 0,
    limit: int = 10,
    type_: str = "single",
    category: str = None,
    quiz_amount: int = None,
    current_user: User = Depends(get_current_user),
):
    return await question.get_many(skip, limit, type_, category, quiz_amount)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_new_questions(
    question_in: QuestionCreate,
    current_user: User = Depends(get_current_active_superuser),
):
    question_dict = question_in.dict(exclude={"options"})
    list_of_option_dict = [option.dict() for option in question_in.options]
    new_generated_question_id = await question.create(QuestionInDB(**question_dict))
    for option_dict in list_of_option_dict:
        try:
            option_dict.update({"question_id": new_generated_question_id})
            new_generated_option_id = await option.create(OptionInDB(**option_dict))
        except NotImplementedError:
            await question.remove(new_generated_question_id)
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Could not create"
            )
    return {
        "id": new_generated_question_id,
        **question_dict,
        "options": [
            OptionOut(**option_dict, id=new_generated_option_id)
            for option_dict in list_of_option_dict
        ],
    }


# @router.post("/")
