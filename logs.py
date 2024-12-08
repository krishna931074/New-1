# logs.py

import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime, timedelta

# Set up logging
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler("logs.txt", maxBytes=50000000, backupCount=10),
        logging.StreamHandler(),
    ],
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# Initialize logger
logger = logging.getLogger()

def get_last_two_minutes_logs():
    two_minutes_ago = datetime.now() - timedelta(minutes=2)
    logs = []

    with open("logs.txt", "r") as file:
        for line in file:
            try:
                log_time_str = line.split(" - ")[0]
                log_time = datetime.strptime(log_time_str, "%d-%b-%y %H:%M:%S")
                if log_time >= two_minutes_ago:
                    logs.append(line)
            except ValueError:
                continue

    return logs
