import argparse
import sys
import os
import time


current_dir = os.path.dirname(__file__)
# Move one folder up
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(parent_dir)
from db.pinterest import PinterestLinkDatabase
from services.pin_service import PinService
from socials import social
import utils
import random


def post_on_social(post_type, limit):
    db = PinterestLinkDatabase()
    pin_service = PinService()
    definitions = db.get_items(limit=limit)
    for definition in definitions:
        id = definition[0]
        post_id = definition[1]
        link = definition[2]
        title = definition[3]
        description = definition[4]
        media_url = definition[5]
        board_id = definition[6]
        section_id = definition[7]
        alt_text = definition[8]
        keywords = definition[8]

        result = pin_service.create_pin_from_db(
            link=link,
            title=title,
            description=description,
            media_url=media_url,
            board_id=board_id,
            section_id=section_id,
            alt_text=alt_text,
        )
        if result is False:
            print("Error occured")
            break
        else:
            db.set_as_published(id)
            print(f"created: {post_id} : {title}")
            random_sleep = random.randint(60, 240)
            time.sleep(random_sleep)
    return "Stopped"


if __name__ == "__main__":
    # Generate a random sleep duration between 180 and 240 seconds (3 to 4 minutes)
    # random_sleep = random.randint(120, 420)

    # time.sleep(random_sleep)
    parser = argparse.ArgumentParser(
        description="Post on social media using definitions and IDs."
    )
    parser.add_argument("post_type", type=str, help="The type of post to be made.")
    parser.add_argument("limit", type=str, help="Number of pins to be created")

    args = parser.parse_args()
    result = post_on_social(args.post_type, args.limit)
