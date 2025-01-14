import json
from .base_entity import BaseEntity
from .llm_string_convertible import LLMStringConvertible
import os

class UserData(BaseEntity, LLMStringConvertible):
  def __init__(self, name: str, birthday: str, sex: str, race: str, lat: int, lon: int, details: str = "", weather_enabled: bool = False, chess_enabled: bool = False):
    super().__init__(name, birthday, sex, race, lat, lon)
    self.details: str = details
    self.weather_enabled: bool = weather_enabled
    self.chess_enabled: bool = chess_enabled

  def to_dict(self) -> dict:
    return {
      "name": self.name,
      "birthday": self.birthday,
      "sex": self.sex,
      "race": self.race,
      "lat": self.lat,
      "lon": self.lon,
      "details": self.details,
      "weather_enabled": self.weather_enabled,
      "chess_enabled": self.chess_enabled
    }

  @staticmethod
  def from_dict(data: dict) -> "UserData":
    user_data = data.get("user_data", {})
    features = data.get("features", {})
    return UserData(
      name=user_data["name"],
      birthday=user_data["birthday"],
      sex=user_data["sex"],
      race=user_data["race"],
      lat=user_data["lat"],
      lon=user_data["lon"],
      details=user_data.get("details", ""),
      weather_enabled=features.get("weather_enabled", False),
      chess_enabled=features.get("chess_enabled", False)
    )

  def to_llm_string(self) -> str:
    return (
      f"Name: {self.name}\n"
      f"Birthday: {self.birthday}\n"
      f"Sex: {self.sex}\n"
      f"Race: {self.race}\n"
      f"Lat: {self.lat}\n"
      f"Lon: {self.lon}\n"
      f"Details: {self.details if self.details else 'N/A'}\n"
    )

  @classmethod
  def from_json_file(cls) -> "UserData":
    config_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "config"))
    filepath = os.path.abspath(os.path.join(config_dir, "config.json"))

    if not os.path.exists(filepath):
      raise FileNotFoundError(f"Configuration file '{filepath}' not found.")
    
    try:
      with open(filepath, 'r') as file:
        data = json.load(file)
        return cls.from_dict(data)
    except json.JSONDecodeError:
      raise ValueError(f"Failed to decode JSON from the file '{filepath}'. Please check the file format.")
    except Exception as e:
      raise RuntimeError(f"An unexpected error occurred: {str(e)}")