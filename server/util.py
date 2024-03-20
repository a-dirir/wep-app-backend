from binascii import hexlify, unhexlify
from time import time
from hashlib import sha256
import logging
from os import path, getenv


def get_logger(name):

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s %(message)s",
                                  datefmt="%Y-%m-%d %H:%M:%S")

    log_dir = getenv("LOG_DIR")
    if log_dir is None:
        log_dir = ''

    success = logging.FileHandler(path.join(log_dir, "success.log"), "a")
    success.setLevel(logging.INFO)
    success.setFormatter(formatter)

    error = logging.FileHandler(path.join(log_dir, "error.log"), "a")
    error.setLevel(logging.ERROR)
    error.setFormatter(formatter)

    logger.addHandler(success)
    logger.addHandler(error)

    return logger


def c2s(msg):
    return str(hexlify(msg), encoding='utf8')


def c2b(msg):
    return unhexlify(bytes(msg, encoding='utf8'))


def get_current_time():
    return int(time())


def get_time_difference(given_time):
    return int(given_time - time())


def hash_msg(msg):
    return sha256(msg).digest()


