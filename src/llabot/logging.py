import logging
import os
from datetime import datetime
from colorama import Fore, Style

# Create 'log' directory if it doesn't exist
LOG_DIR = "log"
os.makedirs(LOG_DIR, exist_ok=True)

# Define log level colors
LOG_LEVEL_COLORS = {
    "DEBUG": Fore.BLUE,
    "INFO": Fore.GREEN,
    "WARNING": Fore.YELLOW,
    "ERROR": Fore.RED,
    "CRITICAL": Fore.MAGENTA,
}

class ColoredFormatter(logging.Formatter):
    def format(self, record):
        # Get color for the log level
        levelname = record.levelname
        color = LOG_LEVEL_COLORS.get(levelname, Fore.WHITE)
        
        # Format module and function name dynamically
        module_name = record.module
        func_name = record.funcName
        
        # Apply custom format
        message = f"[{Style.RESET_ALL}{color}{levelname}{Style.RESET_ALL}][{module_name}][{func_name}] {record.getMessage()}"
        return message

class CustomLogger:
    def __init__(self, name, console=True, file=True):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Prevent duplicate log entries
        if not self.logger.handlers:
            # Console handler
            if console:
                console_handler = logging.StreamHandler()
                console_handler.setLevel(logging.DEBUG)
                console_handler.setFormatter(ColoredFormatter())
                self.logger.addHandler(console_handler)

            # File handler
            if file:
                log_file = os.path.join(LOG_DIR, f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
                file_handler = logging.FileHandler(log_file)
                file_handler.setLevel(logging.DEBUG)
                file_handler.setFormatter(logging.Formatter("[%(levelname)s][%(module)s][%(funcName)s] %(message)s"))
                self.logger.addHandler(file_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

# Usage example
if __name__ == "__main__":
    logger = CustomLogger("MyLogger", console=True, file=True)
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")