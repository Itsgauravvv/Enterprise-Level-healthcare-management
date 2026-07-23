import logging
import os
logger = logging.getLogger(__name__)

if not os.path.exists("logs"):
    os.makedirs("logs")
logging.basicConfig(
    filename="logs/healthcare.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S"
)
def log_info(message):
    """Log information messages."""
    logging.info(message)
def log_warning(message):
    """Log warning messages."""
    logging.warning(message)
def log_error(message):
    """Log error messages."""
    logging.error(message)
def log_critical(message):
    """Log critical messages."""
    logging.critical(message)
def log_debug(message):
    """Log debug messages."""
    logging.debug(message)