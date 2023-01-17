import logging
from my_logger import get_logger

logger = get_logger(__name__)


def baz(el: str):
    logger.info("Start function baz")
    logger.debug(f"el={el}")


def foo():
    logger.error("Exception!")


if __name__ == "__main__":
    logger.log(logging.DEBUG, "Start")
    baz("test")
    foo()
