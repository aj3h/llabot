from dataclasses import dataclass
from typing import Dict
import json
import os

@dataclass
class SceneData:
    setting: str
    characters: list[str]
    relationship: str
    tone: str

    def to_dict(self) -> Dict[str, any]:
        return {
            'setting': self.setting,
            'characters': self.characters,
            'relationship': self.relationship,
            'tone': self.tone
        }

    @staticmethod
    def from_dict(data: Dict[str, any]) -> 'SceneData':
        return SceneData(
            setting=data['setting'],
            characters=data.get('characters'),
            relationship=data['relationship'],
            tone=data['tone']
        )

    @classmethod
    def load_from_file(self, filename: str = 'config/scene.json') -> 'SceneData':
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), filename))
        with open(file_path, 'r') as file:
            data = json.load(file)
        return SceneData.from_dict(data)

    def to_llm_string(self) -> str:
        return f"Setting: {self.setting}\nCharacters: {self.characters}\nRelationship: {self.relationship}\nTone: {self.tone}"