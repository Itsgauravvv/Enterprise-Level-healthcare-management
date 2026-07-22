import logging

logger = logging.getLogger("HealthcareManagementSystem")
logger.setLevel(logging.INFO)

if not logger.handlers:

    file_handler = logging.FileHandler("healthcare.log")
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)