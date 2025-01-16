from flask import Blueprint, request, session
from pinterest.pin import fetch_pins_from_board
from utils_old import load_env_vars, save_tokens_to_env, get_env_var

content_blueprint = Blueprint("content", __name__)
# board_service = BoardService()
