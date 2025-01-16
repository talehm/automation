import json
import os
from abc import ABC, abstractmethod
from typing import List


class PostStorage(ABC):
    @abstractmethod
    def load_posted_ids(self) -> List[str]:
        pass

    @abstractmethod
    def save_posted_ids(self, data: List[str]) -> None:
        pass


class JsonFileStorage(PostStorage):
    def __init__(self, social_platform: str):
        current_dir = os.path.dirname(__file__)
        parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
        self.file_path = os.path.join(
            parent_dir, "social_media/data", f"{social_platform}_ids.json"
        )

    def load_posted_ids(self) -> List[str]:
        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_posted_ids(self, data: List[str]) -> None:
        with open(self.file_path, "w") as file:
            json.dump(data, file)
