import logging
import json
import os
import time

from uuid import uuid4

import boto3
import redis
from fastapi import FastAPI, HTTPException, Request

from src import models as app_models

QUEUE_NAME = os.getenv("QUEUE_NAME", "question-queue")

time.sleep(10)


app = FastAPI()
logger = logging.getLogger()
logger.setLevel(os.getenv("LOG_LEVEL", "INFO").upper())
logger.info(f"Starting FastAPI server with QUEUE_NAME: {QUEUE_NAME}")


try:
    aws_session = boto3.Session(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_DEFAULT_REGION"),
    )
    logger.info(f"Connected to AWS: {aws_session}")
    sqs = aws_session.client("sqs", endpoint_url=os.getenv("ENDPOINT_URL"))
    queue = sqs.get_queue_url(QueueName=QUEUE_NAME)
    logger.info(f"Connected to SQS: {queue}")
except Exception as e:
    logger.error(f"Failed to connect to SQS: {e}", exc_info=True)
    raise e

try:
    redis_client = redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", "6379")),
        password=os.getenv("REDIS_PASSWORD"),
    )
    logger.info(f"Connected to Redis: {redis_client}")
except Exception as e:
    logger.error(f"Failed to connect to Redis: {e}", exc_info=True)
    raise e


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/question", response_model=app_models.QuestionResponse)
async def question(question: app_models.Question):
    job_id = uuid4()
    message_body = question.model_dump()
    message_body["job_id"] = str(job_id)
    try:
        response = sqs.send_message(
            QueueUrl=queue.get("QueueUrl"),
            MessageBody=json.dumps(message_body),
        )
        logger.info(f"Sent message to SQS: {response.get('MessageId')}")
        logger.info(f"Sent message to SQS: {message_body}")
    except Exception as e:
        logger.error(f"Failed to send message to SQS: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to post job question")
    return app_models.QuestionResponse(jobId=job_id)


@app.post("/answer", response_model=app_models.AnswerResponse)
async def answer(answer: app_models.Answer):
    try:
        result = redis_client.get(str(answer.job_id))
        if result is None:
            raise HTTPException(status_code=404, detail="Job ID not found")
        logger.debug(f"Got answer from Redis: {result}")
        response = json.loads(result.decode("utf-8"))
        response = app_models.AnswerResponse(
            jobId=answer.job_id,
            question=response.get("question"),
            answer=response.get("answer"),
        )
    except Exception as e:
        logger.error(f"Failed to get answer: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to post job answer")
    return response
