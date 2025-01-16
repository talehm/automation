import json
import os
from typing import Set, List, Dict, Any
from abc import ABC, abstractmethod


class FileHandler(ABC):
    @abstractmethod
    def read(self) -> Any:
        pass

    @abstractmethod
    def write(self, data: Any) -> None:
        pass


class JsonFileHandler(FileHandler):
    def __init__(self, file_path: str = "default.json"):
        self.file_path = file_path

    def read(self) -> Any:
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, "r", encoding="utf-8") as file:
                    return json.load(file)
        except FileNotFoundError:
            return []

    def write(self, data: Any) -> None:
        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)


class ArticleIdManager:
    def __init__(self, file_handler: FileHandler):
        self.file_handler = file_handler

    def read_existing_ids(self) -> Set[str]:
        data = self.file_handler.read()
        return {entry["id"] for entry in data} if data else set()

    def write_article_id(self, article_id: str) -> None:
        data = self.file_handler.read() or []
        data.append({"id": article_id})
        self.file_handler.write(data)
