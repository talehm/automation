from typing import Optional, Dict, List
from db.pinterest import PinterestLinkDatabase
from utils.html_processor import HtmlProcessor
from utils.file_handler import JsonFileHandler
from utils.content_filter import ContentFilter
from services.board_service import BoardService
from services.pin_service import PinService
from services.csv_service import CSVService
from services.image_service import ImageService
import json
import random
import time

from wordpress.post_manager import PostManager


class DefinitionService:
    """Handles all definition-related operations."""

    def __init__(self):
        self.board_service = BoardService()
        self.pin_service = PinService()
        self.csv_service = CSVService()
        self.image_service = ImageService()
        self.file_handler = JsonFileHandler()
        self.content_file = ContentFilter(self.file_handler)

    def create_definitions(self, mode: Optional[str] = None) -> str:
        """Create definition pins based on mode."""
        board = self.board_service.get_boards("definitions")
        if not board:
            return "Board not found"

        try:
            definitions = self.file_handler("data/result.json").read()
            template_folder = f"./image/templates/{board['name']}"

            for index, definition in enumerate(definitions):
                if mode != "db" and index >= 10:
                    break

                if self._should_skip_definition(mode, definition):
                    continue

                result = self._process_definition(
                    definition, template_folder, board, mode, index
                )
                if not result:
                    break

        except Exception as e:
            print(f"Error creating definitions: {e}")
            return str(e)

        return "Finished!"

    def extract_definitions(self) -> str:
        """Extract and process definitions."""
        board = self.board_service.get_boards("definitions")
        if not board:
            return "Board not found"

        self.pin_service.fetch_pins_from_board(board["id"])
        PostManager.fetch_pins("definition")
        self._filter_definitions()
        return "True"

    def _should_skip_definition(self, mode: str, definition: Dict) -> bool:
        """Check if definition should be skipped."""
        if mode == "db":
            db = PinterestLinkDatabase()
            return db.exists(definition["id"])
        return False

    def _process_definition(
        self, definition: Dict, template_folder: str, board: Dict, mode: str, index: int
    ) -> bool:
        """Process a single definition."""
        item = self.pin_service.fetch_by_id("definition", definition["id"])
        if not item:
            return True

        content = self._parse_content(item)
        if not content:
            return True

        result = random.choice(content["results"])
        image_url = self.image_service.generate_and_upload(
            template_folder, item, result
        )

        if not image_url:
            return False

        item["pinterest_media"] = image_url
        return self._handle_pin_creation(mode, item, content, board, index)

    def _parse_content(self, item: Dict) -> Optional[Dict]:
        """Parse definition content."""
        content = HtmlProcessor.fromHtml(item["content"]["rendered"])
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return None

    def _handle_pin_creation(
        self, mode: str, item: Dict, content: Dict, board: Dict, index: int
    ) -> bool:
        """Handle pin creation based on mode."""
        if mode == "db":
            return self.pin_service.create_pin_from_db(item, content, board)
        elif mode == "csv":
            return self.csv_service.create_csv(item, content, board, index)
        else:
            return self.pin_service.create_pin(item, board)

    def _filter_definitions(self):
        """Filter definitions based on title."""
        self.content_file.filter_by_title(
            "data/pins.json", "data/definitions.json", "data/result.json"
        )
