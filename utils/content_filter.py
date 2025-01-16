from typing import List, Dict
from .file_handler import JsonFileHandler


class ContentFilter:
    def __init__(self, file_handler: JsonFileHandler):
        self.file_handler = file_handler

    def filter_by_title(
        self, filter_file: str, main_file: str, output_file: str
    ) -> None:
        self.file_handler.file_path = filter_file
        pins = self.file_handler.read()
        definitions = JsonFileHandler(main_file).read()
        pin_titles = {pin["title"] for pin in pins}
        filtered_definitions = [
            definition
            for definition in definitions
            if definition["title"] not in pin_titles
        ]
        JsonFileHandler(output_file).write(filtered_definitions)
