import logging
from logging import Logger

import boto3
from config import conf
from watchtower import CloudWatchLogHandler


def get_cloudwatch_handler():
    return CloudWatchLogHandler(
        log_group="test",
        stream_name="test logs",
        boto3_client=boto3.client(
            "logs",
            aws_access_key_id=conf.LOG_AWS_ACCESS_KEY,
            aws_secret_access_key=conf.LOG_AWS_SECRET_ACCESS_KEY,
            region_name="us-east-1",
        ),
    )


def get_logger(logger_name: str, log_level: int = logging.INFO) -> Logger:
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)

    if not logger.handlers:
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        cloudwatch_handler = get_cloudwatch_handler()
        cloudwatch_handler.setFormatter(formatter)

        logger.addHandler(stream_handler)
        logger.addHandler(get_cloudwatch_handler())

    return logger
