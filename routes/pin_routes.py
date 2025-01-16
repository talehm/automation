from flask import Blueprint, session, request
from services.pin_service import PinService
from services.board_service import BoardService
from services.csv_service import CSVService
from services.image_service import ImageService
from services.definition_service import DefinitionService
from utils.env_manager import EnvManager
from db.pinterest import PinterestLinkDatabase


class PinRouteHandler:
    """Handles all pin-related routes."""

    def __init__(self):
        self.pin_service = PinService()
        self.board_service = BoardService()
        self.csv_service = CSVService()
        self.image_service = ImageService()
        self.definition_service = DefinitionService()

    def setup_routes(self, blueprint: Blueprint):
        """Set up all routes for the pins blueprint."""
        blueprint.route("/house/<cat_id>")(self.create_house)
        blueprint.route("/create/<board>/<cat_id>")(self.create)
        blueprint.route("/definition/<mode>", methods=["GET"])(self.create_definitions)
        blueprint.route("/definition", methods=["GET"])(self.create_definitions)
        blueprint.route("/extract/definition/", methods=["GET"])(
            self.extract_definitions
        )

    def create_house(self, cat_id):
        """Handle house pin creation."""
        session["access_token"] = EnvManager.get_env_var("ACCESS_TOKEN")
        return self.pin_service.create_house_pins(cat_id)

    def create(self, board, cat_id):
        """Handle general pin creation."""
        session["access_token"] = EnvManager.get_env_var("ACCESS_TOKEN")
        return self.pin_service.create_board_pins(board, cat_id)

    def create_definitions(self, mode=None):
        """Handle definition pin creation."""
        if request.method != "GET":
            return "", 405
        session["access_token"] = EnvManager.get_env_var("ACCESS_TOKEN")
        return self.definition_service.create_definitions(mode)

    def extract_definitions(self):
        """Handle definition extraction."""
        if request.method != "GET":
            return "", 405
        session["access_token"] = EnvManager.get_env_var("ACCESS_TOKEN")
        return self.definition_service.extract_definitions()


# Create blueprint instance
pins_bp = Blueprint("pins", __name__)
route_handler = PinRouteHandler()
route_handler.setup_routes(pins_bp)
