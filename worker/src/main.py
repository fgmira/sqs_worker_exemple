import logging
import json
import os
import time


import boto3
import redis
from openai import OpenAI


QUEUE_NAME = os.getenv("QUEUE_NAME", "question-queue")
time.sleep(10)
logger = logging.getLogger()
logger.setLevel(os.getenv("LOG_LEVEL", "INFO").upper())

logger.info(f"Starting worker with QUEUE_NAME: {QUEUE_NAME}")

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


def main():
    client_oai = OpenAI()
    while True:
        try:
            response = sqs.receive_message(
                QueueUrl=queue.get("QueueUrl"),
                MaxNumberOfMessages=1,
                WaitTimeSeconds=20,
            )
        except Exception as e:
            logger.error(f"Failed to receive message from SQS: {e}", exc_info=True)
            raise e
        if "Messages" in response:
            logger.debug(f"Received message from SQS: {response}")
            for message in response["Messages"]:
                message_body = json.loads(message["Body"])
                logger.info(f"Received message from SQS: {message_body}")
                question = message_body.get("question")

                try:
                    answer = client_oai.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {
                                "role": "system",
                                "content": "The following is a conversation with an AI assistant.",
                            },
                            {"role": "user", "content": question},
                        ],
                    )
                    logger.info(f"Received answer from OpenAI: {answer}")
                except Exception as e:
                    logger.error(
                        f"Failed to get answer from OpenAI: {e}", exc_info=True
                    )
                    raise e
                try:
                    redis_client.set(
                        message_body.get("job_id"),
                        json.dumps(
                            {
                                "question": question,
                                "answer": answer.choices[0].message.content,
                            }
                        ),
                    )
                    logger.info(f"Saved answer to Redis: {message_body.get('job_id')}")
                except Exception as e:
                    logger.error(f"Failed to save answer to Redis: {e}", exc_info=True)
                    raise e
                try:
                    sqs.delete_message(
                        QueueUrl=queue.get("QueueUrl"),
                        ReceiptHandle=message["ReceiptHandle"],
                    )
                    logger.info(f"Deleted message from SQS: {message}")
                except Exception as e:
                    logger.error(
                        f"Failed to delete message from SQS: {e}", exc_info=True
                    )
                    raise e


if __name__ == "__main__":
    main()
