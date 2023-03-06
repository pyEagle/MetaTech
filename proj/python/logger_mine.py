# -*- coding:utf-8 -*-

import logging

from logging import handlers


def logger(log_file):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = handlers.TimedRotatingFileHandler(log_file,
                                       when="D",
                                       interval=1,
                                       backupCount=7)
    formatter = logging.Formatter(
        "%(asctime)s - %(funcName)s- %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
