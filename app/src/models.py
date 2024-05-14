from uuid import UUID
from typing import List, Optional
from pydantic import BaseModel, Field


class Question(BaseModel):
    question: str = Field(
        ...,
        title="Question",
        description="The question to ask",
        examples=["What is the capital of France?"],
    )


class QuestionResponse(BaseModel):
    job_id: UUID = Field(
        ...,
        alias="jobId",
        title="Job ID",
        description="The job ID of the question",
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    )


class Answer(BaseModel):
    job_id: UUID = Field(
        ...,
        alias="jobId",
        title="Job ID",
        description="The job ID of the question",
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    )


class AnswerResponse(BaseModel):
    job_id: UUID = Field(
        ...,
        alias="jobId",
        title="Job ID",
        description="The job ID of the question",
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    )
    question: str = Field(
        ...,
        title="Question",
        description="The question that was asked",
        examples=["What is the capital of France?"],
    )
    answer: str = Field(
        ...,
        title="Answer",
        description="The answer to the question",
        examples=["Paris"],
    )
