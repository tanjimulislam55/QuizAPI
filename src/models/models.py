from sqlalchemy.orm import relationship
from sqlalchemy import Column, Float, Integer, String, Boolean, ForeignKey, Date, Text

from .base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    username = Column(String(50), nullable=False, unique=True, index=True)
    email = Column(String(100), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)
    is_superuser = Column(Boolean, default=False)

    question_answers = relationship("QuestionAnswer", back_populates="user")


class Question(BaseModel):
    __tablename__ = "questions"

    question = Column(String(255), nullable=False)
    quiz_amount = Column(Integer)
    category = Column(String(20))
    type_ = Column(String(20))

    options = relationship("Option", back_populates="question")
    question_answers = relationship("QuestionAnswer", back_populates="question")


class Option(BaseModel):
    __tablename__ = "options"

    option = Column(String)
    is_correct_option = Column(Boolean, default=False)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"))

    question = relationship("Question", back_populates="options")
    question_answers = relationship("QuestionAnswer", back_populates="option")


class QuestionAnswer(BaseModel):
    __tablename__ = "question_answers"

    is_right = Column(Boolean)
    user_id = Column(Integer, ForeignKey("users.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    option_id = Column(Integer, ForeignKey("options.id"))

    user = relationship("User", back_populates="question_answers")
    question = relationship("Question", back_populates="question_answers")
    option = relationship("Option", back_populates="question_answers")
