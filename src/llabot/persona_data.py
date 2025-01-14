import json
import os
from .base_entity import BaseEntity
from .llm_string_convertible import LLMStringConvertible
from . import logger

class PersonaData(BaseEntity, LLMStringConvertible):
    def __init__(self, persona_name: str):
      self.load_persona_data(persona_name)
    
    def load_persona_data(self, persona_name: str):
      """Loads persona data from a JSON file."""
      logger.debug("Persona data is being loaded.")
      persona_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "persona"))
      if not os.path.exists(persona_dir):
          logger.error("Persona directory not found.")
          raise FileNotFoundError(f"'persona' directory not found at: {persona_dir}. Program cannot run without persona files.")
      named_dir = os.path.abspath(os.path.join(persona_dir, f"{persona_name}"))
      if not os.path.exists(named_dir):
          logger.error("Named persona directory not found.")
          raise FileNotFoundError(f"'{persona_name}' directory not found at: {named_dir}. Program cannot run without persona files.")
      file_path = os.path.abspath(os.path.join(named_dir, f"{persona_name}.json"))
      
      if not os.path.exists(file_path):
        raise FileNotFoundError(f"Persona data file '{file_path}' not found.")
      
      with open(file_path, 'r') as file:
        data = json.load(file)

      core_identity = data["core_identity"]
      self.name = core_identity["name"]
      self.birthday = core_identity["birthday"]
      self.sex = core_identity["sex"]
      self.race = core_identity["race"]
      self.lat = core_identity["lat"]
      self.lon = core_identity["lon"]

      self.physical_form = data.get("physical_form", {})

      self.mind = data.get("psychology", {})

      self.social_connections = data.get("history", {}).get("relationships", {})

      self.communication = data.get("communication", {})

      self.knowledge = data.get("knowledge", {})

      self.hobbies_and_passions = data.get("hobbies_and_passions", {})

      self.skills = data.get("skills", {})
      logger.debug("Presumably persona data was loaded.")

    def to_dict(self) -> dict:
      """Convert the PersonaData object to a dictionary."""
      return {
        "name": self.name,
        "birthday": self.birthday,
        "sex": self.sex,
        "race": self.race,
        "lat": self.lat,
        "lon": self.lon,
        "physical_form": self.physical_form,
        "mind": self.mind,
        "social_connections": self.social_connections,
        "communication": self.communication,
        "knowledge": self.knowledge,
        "hobbies_and_passions": self.hobbies_and_passions,
        "skills": self.skills,
      }

    @staticmethod
    def from_dict(data: dict) -> "PersonaData":
      """Create a PersonaData object from a dictionary."""
      persona_name = data["name"]
      persona = PersonaData(persona_name)
      persona.name = data["name"]
      persona.birthday = data["birthday"]
      persona.sex = data["sex"]
      persona.race = data["race"]
      persona.lat = data["lat"]
      persona.lon = data["lon"]
      persona.physical_form = data.get("physical_form", {})
      persona.mind = data.get("mind", {})
      persona.social_connections = data.get("social_connections", {})
      persona.communication = data.get("communication", {})
      persona.knowledge = data.get("knowledge", {})
      persona.hobbies_and_passions = data.get("hobbies_and_passions", {})
      persona.skills = data.get("skills", {})
      return persona
    
    def to_llm_string(self) -> str:
      """Converts the PersonaData object to a human-readable string for LLMs."""
      lines = [
        f"Name: {self.name}",
        f"Birthday: {self.birthday}",
        f"Sex: {self.sex}",
        f"Race: {self.race}",
        f"Lat: {self.lat}",
        f"Lon: {self.lon}",
        "\nPhysical Form:",
      ]
      for key, value in self.physical_form.items():
        lines.append(f"  {key.capitalize()}: {value}")
      
      lines.append("Mind:")
      for key, value in self.mind.items():
        if isinstance(value, list):
          lines.append(f"  {key.capitalize()}: {', '.join(value)}")
        else:
          lines.append(f"  {key.capitalize()}: {value}")
      
      lines.append("Social Connections:")
      for category, connections in self.social_connections.items():
          if isinstance(connections, dict):
            lines.append(f"  {category.capitalize()}:")
            for relation, names in connections.items():
              if isinstance(names, list):
                lines.append(f"    {relation.capitalize()}: {', '.join(names)}")
              else:
                lines.append(f"    {relation.capitalize()}: {names}")
          elif isinstance(connections, list):
            lines.append(f"  {category.capitalize()}: {', '.join(connections)}")
          else:
            lines.append(f"  {category.capitalize()}: {connections}")
      
      # Adding communication data
      lines.append("Communication:")
      for key, value in self.communication.items():
        lines.append(f"  {key.capitalize()}: {value}")

      # Adding knowledge data
      lines.append("Knowledge:")
      for key, value in self.knowledge.items():
        lines.append(f"  {key.capitalize()}: {value}")
      
      # Adding hobbies and passions data
      lines.append("Hobbies & Passions:")
      for key, value in self.hobbies_and_passions.items():
        lines.append(f"  {key.capitalize()}: {', '.join(value)}")
      
      # Adding skills data
      lines.append("Skills:")
      for key, value in self.skills.items():
        lines.append(f"  {key.capitalize()}: {value}")
      
      return "\n".join(lines)