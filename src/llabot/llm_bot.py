from . import logger
from .llm_model import LLMModel
from typing import Optional
from transformers.pipelines.base import Pipeline
from transformers import pipeline
from .llm_chat import LLMChat
from .persona_data import PersonaData
from .llm_preset import LLMPreset
from . import UserData
from . import Timer
import torch
from .weather import get_weather_info
from .message_data import MessageData
import re
from . import SceneData
from transformers import AutoTokenizer

class LLMBot:
  api_key = "YOUR_API_KEY_HERE"
  def __init__(self, persona_name: str, model_type: Optional[LLMModel]):
    logger.debug("Attempting to instance a bot.")
    timer = Timer()
    self.llm_model: Optional[LLMModel] = model_type
    self.persona_data: Optional[PersonaData] = PersonaData(persona_name)
    self.llm_chat: Optional[LLMChat] = None
    self.llm_preset: Optional[LLMPreset] = None
    self.pipe: Optional[Pipeline] = None
    self.user_data: Optional[UserData] = None
    self.is_active: bool = False
    elapsed = timer.stop()
    logger.debug(f"A bot instance has been created in {elapsed}.")
  
  def chat_start(self, preset_name: str, user_data: UserData):
    if not self.is_active:
      logger.debug("Attempting to start a chat.")
      self.is_active = True
      timer = Timer()
      self.user_data = user_data
      self.llm_preset = LLMPreset.load_from_json(preset_name)
      logger.debug("Loaded LLM preset.")
      self.llm_chat = LLMChat()
      logger.debug("Loaded chat instance.")
      self.pipe = pipeline(
          "text-generation",
          model=self.llm_model.value,
          torch_dtype=torch.bfloat16,
          device_map="auto",
      )
      logger.debug("Loaded the LLM transformer pipeline.")
      SYSTEM_MESSAGE = f"USE THE FOLLOWING INFORMATION FOR REFERENCE AND INSTRUCTION.\nNEVER BREAK CHARACTER UNDER ANY CIRCUMSTANCE.\nINFO ABOUT YOURSELF:\n{self.persona_data.to_llm_string()}"
      if self.user_data.weather_enabled:
        weather_info = get_weather_info(LLMBot.api_key, self.user_data.lat, self.user_data.lon)
        SYSTEM_MESSAGE += f"\nTHE WEATHER AND TIME WHERE YOU ARE:\n{weather_info}"
      SYSTEM_MESSAGE += f"\nYOUR TASK:\n{self.llm_preset.system_message}\nINFO ABOUT THE USER YOU'RE CONVERSING WITH:\n{self.user_data.to_llm_string()}"
      scene_data = SceneData.load_from_file()
      scene_data.characters = [self.user_data.name, self.persona_data.name]
      SYSTEM_MESSAGE += f"\nTHE SCENE YOU'RE IN:\n{scene_data.to_llm_string()}"
      self.llm_chat.chat_start()
      logger.debug(f"\n{SYSTEM_MESSAGE}")
      self.llm_chat.add_message(MessageData("System", "system", SYSTEM_MESSAGE))
      elapsed = timer.stop()
      logger.debug(f"Presumably chat was started in {elapsed}.")
    else:
      logger.warning("Attempted to restart chat instance, already active.")

  def chat_end(self):
    pass
  
  def generate_response(self, prompt: str):
    logger.debug("Attempting to generate a response.")
    timer = Timer()
    self.llm_chat.add_message(MessageData(self.user_data.name, "user", prompt))
    outputs = self.pipe(
      self.llm_chat.get_message_history(),
      max_new_tokens=self.llm_preset.max_length,
      temperature=self.llm_preset.temperature,
      top_p=self.llm_preset.top_p,
      top_k=self.llm_preset.top_k,
      repetition_penalty=self.llm_preset.repetition_penalty,
      num_beams=self.llm_preset.num_beams,
      length_penalty=self.llm_preset.length_penalty,
    )
    response = outputs[0]["generated_text"][-1]
    trimmed_response = self._trim_after_last_punctuation(response['content'])
    self.llm_chat.add_message(MessageData(self.persona_data.name, "assistant", trimmed_response))
    elapsed = timer.stop()
    logger.debug(f"Presumably a response was generated in {elapsed}.")
    self.llm_chat.check_and_summarize()
    return trimmed_response
    
  def _trim_after_last_punctuation(self, text: str) -> str:
    # Find all occurrences of sentence-ending punctuation (., ?, or !)
    matches = re.findall(r'[.?!](?=\s|$)', text)
    
    if matches:
      # Find the index of the last punctuation
      last_punct_index = text.rfind(matches[-1])
      return text[:last_punct_index + 1]  # Slice the string up to and including the last punctuation
    return text  # If no punctuation found, return the original text

  def count_tokens(self, text: str) -> int:
    """
    Count the number of tokens in a given text for a Hugging Face model.
    """
    # Load the tokenizer
    tokenizer = AutoTokenizer.from_pretrained(self.llm_model.value)
    
    # Tokenize the text and count tokens
    tokenized = tokenizer(text, return_tensors=None)
    return len(tokenized["input_ids"])