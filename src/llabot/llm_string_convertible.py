from abc import ABC, abstractmethod

class LLMStringConvertible(ABC):
  @abstractmethod
  def to_llm_string(self) -> str:
    pass