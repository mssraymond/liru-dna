"""
Custom Logger class.
"""

import logging


class Logger:
    def __init__(self) -> None:
        logging.basicConfig(
            level=logging.INFO,
            format="[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d] %(message)s",
        )

    def info(self, msg: str) -> None:
        logging.info(msg=msg)

    def warning(self, msg: str) -> None:
        logging.warning(msg=msg)

    def error(self, msg: str) -> None:
        logging.error(msg=msg, exc_info=True)

    def debug(self, msg: str) -> None:
        logging.debug(msg=msg)

    def exception(self, msg: str) -> None:
        logging.exception(msg=msg)
