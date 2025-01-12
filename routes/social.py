from flask import Blueprint
import socials.social as social
import utils

social_bp = Blueprint("socials", __name__)


@social_bp.route("/social/<post_type>/<soc>", methods=["GET"])
def post_on_social(post_type, soc):
    definitions = utils.load_from_json("data/definitions.json")
    ids = utils.load_from_json(f"socials/{soc}_ids.json")
    count = 1
    for definition in definitions:
        if definition["id"] not in ids:
            social.run(post_type, definition["id"], soc, count)
            count += 1
    return "Stopped"
