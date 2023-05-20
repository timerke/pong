import logging


def set_logger() -> None:
    logging.basicConfig(format="[%(asctime)s %(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S",
                        level=logging.INFO)
