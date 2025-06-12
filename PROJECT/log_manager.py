import logging

def setup_logger():
    logger = logging.getLogger("visa_app")
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler("application.log")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(handler)
    return logger
