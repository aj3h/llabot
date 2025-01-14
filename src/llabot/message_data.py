from datetime import datetime
from typing import Optional, Dict, Any
import uuid
from .llm_string_convertible import LLMStringConvertible
from . import logger

class MessageData(LLMStringConvertible):
  def __init__(self, sender_name: Optional[str] = None, sender_role: Optional[str] = None, message: Optional[str] = None):
    self.timestamp: datetime = datetime.now()
    self.sender_name: str = sender_name
    self.sender_role: str = sender_role
    self.message: str = message
    self.message_id: str = str(uuid.uuid4())
    self.metadata: Dict[str, Any] = {}
    logger.debug(f"A message has been instanced: {self.message_id}.")
    
  def is_valid(self) -> bool:
    return bool(self.message and self.sender_name and self.sender_role)
  
  def add_metadata(self, key: str, value: any) -> None:
    self.metadata[key] = value

  def __eq__(self, other):
    return isinstance(other, MessageData) and self.message_id == other.message_id

  def __lt__(self, other):
    return self.timestamp < other.timestamp
    
  def to_dict(self) -> dict:
    return {
      "timestamp": self.timestamp.isoformat(),
      "sender_name": self.sender_name,
      "sender_role": self.sender_role,
      "message": self.message,
      "message_id": self.message_id,
      "metadata": self.metadata,
    }

  @staticmethod
  def from_dict(data: dict) -> "MessageData":
    instance = MessageData(
      sender_name=data.get("sender_name"),
      sender_role=data.get("sender_role"),
      message=data.get("message"),
    )
    instance.timestamp = datetime.fromisoformat(data["timestamp"])
    instance.message_id = data.get("message_id", str(uuid.uuid4()))
    instance.metadata = data.get("metadata", None)
    return instance
  
  def to_llm_string(self) -> str:
    return (
      f"Message ID: {self.message_id}\n"
      f"Timestamp: {self.timestamp.isoformat()}\n"
      f"Sender: {self.sender_name} ({self.sender_role})\n"
      f"Message: {self.message}\n"
      f"Metadata: {self.metadata if self.metadata else 'N/A'}"
    )