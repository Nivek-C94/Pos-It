import logging
from datetime import datetime
import os

log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, f"posit_{datetime.now().strftime('%Y-%m-%d')}.log")

logging.basicConfig(
    filename=log_file,
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def log_event(message: str):
    logging.info(message)


def log_error(message: str):
    logging.error(message)