from flask import Blueprint
import social_media
from utils.file_handler import JsonFileHandler

social_bp = Blueprint("socials", __name__)

@social_bp.route("/social/<post_type>/<soc>", methods=["GET"])
def post_on_social(post_type, soc):
    file_handler = JsonFileHandler()
    definitions = file_handler.read("data/definitions.json")
    ids = file_handler.read(f"social_media/data/{soc}_ids.json")
    count = 1
    for definition in definitions:
        if definition["id"] not in ids:
            social_media.run(post_type, definition["id"], soc, count)
            count += 1
    return "Stopped"
