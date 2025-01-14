from .llm_bot import LLMBot
from .llm_model import LLMModel
from . import UserData
from .message_data import MessageData
from . import logger

class LLaBot:
  _instance = None
  
  def __new__(cls, *args, **kwargs):
    if not cls._instance:
      cls._instance = super(LLaBot, cls).__new__(cls, *args, **kwargs)
    return cls._instance
  
  def __init__(self):
    if not hasattr(self, 'initialized'):
      self.initialized = True
      self.bot_pool: list[LLMBot] = []
  
  def add_bot(self, persona_name: str = "generic", model_type: LLMModel = LLMModel.SMALL):
    self.bot_pool.append(LLMBot(persona_name, model_type))
    
  def start_chat(self, bot_num: int, user_data: UserData, preset_name: str = "realism"):
    self.bot_pool[bot_num].chat_start(preset_name, user_data)
    
  def generate_response(self, bot_num: int, prompt: str) -> str:
    return self.bot_pool[bot_num].generate_response(prompt)