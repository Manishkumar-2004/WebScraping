import logging
import os
import re

def setup_logger():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    # Find the next available log file name
    existing_logs = [f for f in os.listdir(log_dir) if re.match(r"application\d+\.log", f)]
    log_numbers = [int(re.findall(r"\d+", f)[0]) for f in existing_logs if re.findall(r"\d+", f)]
    next_log_number = max(log_numbers, default=0) + 1
    log_filename = f"application{next_log_number}.log"
    log_path = os.path.join(log_dir, log_filename)

    logger = logging.getLogger("visa_app")
    logger.setLevel(logging.INFO)

    # Avoid duplicate handlers on reruns (in case of imports in Jupyter etc.)
    if logger.hasHandlers():
        logger.handlers.clear()

    handler = logging.FileHandler(log_path)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
