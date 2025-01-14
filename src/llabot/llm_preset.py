from dataclasses import dataclass
from typing import Dict, Any
from . import logger
import json
import os

@dataclass
class LLMPreset:
    # Decoding parameters
    temperature: float = 0.7
    top_k: int = 50
    top_p: float = 0.9
    repetition_penalty: float = 1.0
    max_length: int = 256
    min_length: int = 0
    length_penalty: float = 1.0
    num_beams: int = 1
    
    # Base system message
    system_message: str = "You are a helpful assistant."
    
    def to_dict(self) -> Dict[str, Any]:
        """Converts the configuration to a dictionary."""
        config = self.__dict__.copy()
        config.update(self.additional_args)
        return config

    def __str__(self) -> str:
        """String representation for easy debugging."""
        return str(self.to_dict())
    
    @classmethod
    def load_from_json(cls, preset_name: str) -> 'LLMPreset':
        """Loads a preset from a JSON file and populates the instance with its data."""
        config_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "config"))
        if not os.path.exists(config_dir):
            logger.error("Configuration directory not found.")
            raise FileNotFoundError(f"'config' directory not found at: {config_dir}. Program cannot run without configuration files.")
        else:
            filepath = os.path.abspath(os.path.join(config_dir, "presets.json"))
        try:
            with open(filepath, 'r') as file:
                presets = json.load(file)
            if preset_name not in presets:
                raise ValueError(f"Preset '{preset_name}' not found in {filepath}.")
            return cls(**presets[preset_name])
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{filepath}' not found.")
        except json.JSONDecodeError:
            raise ValueError(f"Error decoding JSON in file '{filepath}'.")