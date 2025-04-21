import logging
import os

log_directory = os.path.join(os.path.dirname(__file__), '..', 'logs', 'produto')
os.makedirs(log_directory, exist_ok=True)

log_file_path = os.path.join(log_directory, 'produto.log')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

if not logger.hasHandlers():
    logger.addHandler(file_handler)
