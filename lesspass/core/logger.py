import os
import logging
from core.settings import BASE_DIR

# Ensure the directory for log files exists
log_dir = BASE_DIR / 'log'
os.makedirs(log_dir, exist_ok=True)

logger = logging.getLogger('logger')
logger.setLevel(logging.INFO)  # Set the desired log level

formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')

file_handler = logging.FileHandler(log_dir / 'custom_logfile.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
