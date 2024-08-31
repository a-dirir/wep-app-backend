import logging
from os import path, getenv


# This function is used to get the logger object
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

