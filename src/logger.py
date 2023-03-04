from datetime import datetime
import logging
import os


LOG_FILE_DIR = os.path.join(os.getcwd(),"logs") ## logs folde is created into the current directory of the project and saved into the object called LOG_FILE_DIR
LOG_FILE_NAME = f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.log" ## This code generates the filename for log files created includes current date and time in  format of month,date,year and hour,minutes and seconds
LOG_FILE_PATH = os.path.join(LOG_FILE_DIR,LOG_FILE_NAME)## joining the logs folder file path and log file name and storing into the LOG_FILE_PATH

logging.basicConfig( #This line of code sets up the basic configuration for Python's built-in logging module.
    filename=LOG_FILE_PATH, # path to the log file where the log messages will be written
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s", # The format of each log message
#%(asctime)s: The time the log message was generated, in a human-readable format.
#%(lineno)d: The line number of the code that generated the log message.
#%(name)s: The name of the logger that generated the log message.
#%(levelname)s: The severity level of the log message (e.g. DEBUG, INFO, WARNING, ERROR, CRITICAL).
#%(message)s: The actual log message.
    level=logging.INFO, #which means that only log messages with a severity level of INFO or higher will be recorded.
)