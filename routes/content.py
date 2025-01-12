from flask import Blueprint, request, session
from pinterest.pin import fetch_pins_from_board
from utils import load_env_vars, save_tokens_to_env, get_env_var
from domain import posts

content_blueprint = Blueprint("content", __name__)
# board_service = BoardService()
