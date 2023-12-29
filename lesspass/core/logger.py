import logging
from core.settings import BASE_DIR

logger = logging.getLogger('logger')
logger.setLevel(logging.INFO)  # Set the desired log level

formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')

file_handler = logging.FileHandler(BASE_DIR / 'log/custom_logfile.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)