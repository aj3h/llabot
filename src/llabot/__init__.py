from .logging import CustomLogger
from .user_data import UserData
from .scene_data import SceneData

logger = CustomLogger("LLaBot", console=True, file=True)

__all__ = ["logger"]

import time

class Timer:
    def __init__(self):
        self.start_time = time.time()  # Start the timer
    
    def stop(self):
        """Stops the timer and returns the elapsed time in the format 'XmYs'."""
        end_time = time.time()  # Stop the timer
        elapsed_time = end_time - self.start_time  # Calculate the elapsed time
        
        minutes = int(elapsed_time // 60)  # Extract minutes
        seconds = int(elapsed_time % 60)  # Extract remaining seconds
        
        # Return the formatted elapsed time as a string
        return f"{minutes}m{seconds}s"

from .llabot import LLaBot