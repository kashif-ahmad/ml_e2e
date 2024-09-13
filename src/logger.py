import logging
import os
from datetime import datetime

## file name (includes timestamp)
LOG_FILE_NAME = f"{datetime.now().strftime ('%m_%d_%Y_%H_%M_%S')}.log"

## get current directory
dir_path = os.path.join(os.getcwd(), "logs", LOG_FILE_NAME)
os.makedirs(dir_path, exist_ok=True)

## complete file name with path
LOG_FILE_PATH = os.path.join(dir_path, LOG_FILE_NAME)

## override the logging function by setting the basic configuration
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s ",
    level=logging.INFO
)


# if __name__== "__main__":
#     logging.info("Logging has started")