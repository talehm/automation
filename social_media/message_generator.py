import json
from abc import ABC, abstractmethod
from typing import Dict


class MessageGenerator(ABC):
    @abstractmethod
    def generate(self, item: Dict) -> str:
        pass


class DefinitionMessageGenerator(MessageGenerator):
    def __init__(self, platform: str):
        self.platform = platform

    def generate(self, item: Dict) -> str:
        if item["type"] != "definition":
            return ""
        brief = ""
        if item["acf"]["brief"] is not None:
            brief = json.loads(item["acf"]["brief"])
        word = item["title"]["rendered"].replace("Definition of ", "")
        hashtags = f"#definition #{word.replace(' ', '')} #meaning #english #ielts"
        if self.platform == "threads":
            return f"{word}\n- {brief[0].capitalize()}\n\n Learn More... \n\n\n #{word.replace(' ', '')}"

        return f"{word}\n- {brief[0].capitalize()}\n\n Learn More... \n\n\n{hashtags}"


class MessageGeneratorFactory:
    @staticmethod
    def create_generator(platform: str) -> MessageGenerator:
        return DefinitionMessageGenerator(platform)
