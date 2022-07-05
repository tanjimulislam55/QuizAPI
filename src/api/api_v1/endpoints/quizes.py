from typing import List, Optional
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from schemas.quizes import (
    QuestionCreate,
    QuestionInDB,
    OptionInDB,
    OptionOut,
    AnswerCreate,
    SubmitAnswer,
)
from models import User
from ...dependencies import get_current_user, get_current_active_superuser
from crud.quizes import question, option, answer

router = APIRouter()


@router.get(
    "/",
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
    questions = await question.get_many(skip, limit, type_, category, quiz_amount)
    question_set = []
    for idx, ques in enumerate(questions):
        question_set.append({"id": ques.id, "question": ques.question, "options": []})
        options = await option.get_many(skip, limit, ques.id)
        for opt in options:
            question_set[idx]["options"].append(OptionOut(**opt))
    return question_set


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_new_questions(
    question_in: QuestionCreate,
    current_user: User = Depends(get_current_active_superuser),
):
    """
    Only superuser can
    create questions
    """
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


@router.post("/answer", status_code=status.HTTP_200_OK)
async def submit_answers(
    submission: List[SubmitAnswer],
    current_user: User = Depends(get_current_active_superuser),
):
    correct_count = 0
    incorrect_count = 0
    marks = 0
    data = []
    for ans in submission:
        opt = await option.get_one(ans.option_id)
        ques = await question.get_one(ans.question_id)
        if opt.is_correct_option == True and opt.question_id == ans.question_id:
            body = {
                "is_right": True,
                "user_id": current_user.id,
                "question_id": ans.question_id,
                "option_id": ans.option_id,
            }
            id = await answer.create(AnswerCreate(**body))
            body.update({"id": id})
            data.append(body)
            correct_count += 1
            marks += ques.quiz_amount
        elif opt.is_correct_option == False:
            body = {
                "is_right": False,
                "user_id": current_user.id,
                "question_id": ans.question_id,
                "option_id": ans.option_id,
            }
            id = await answer.create(AnswerCreate(**body))
            body.update({"id": id})
            data.append(body)
            incorrect_count += 1
            marks -= ques.quiz_amount
    return {
        "submission_data": data,
        "correct_count": correct_count,
        "incorrect_count": incorrect_count,
        "marks_obtained": marks,
    }
