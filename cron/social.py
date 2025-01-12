import argparse
import sys
import os
import time

current_dir = os.path.dirname(__file__)
# Move one folder up
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(parent_dir)
# print(os.path.abspath(os.path.join(os.path.dirname(__file__))))
from socials import social
import utils
import random


def post_on_social(post_type, soc):
    definitions = utils.load_from_json("data/definitions.json")
    ids = utils.load_from_json(f"socials/{soc}_ids.json")
    count = 1
    for definition in definitions:
        if definition["id"] not in ids:
            social.run(post_type, definition["id"], soc, count)
            count += 1
    return "Stopped"


if __name__ == "__main__":
    # Generate a random sleep duration between 180 and 240 seconds (3 to 4 minutes)
    random_sleep = random.randint(60, 240)

    time.sleep(random_sleep)
    parser = argparse.ArgumentParser(
        description="Post on social media using definitions and IDs."
    )
    parser.add_argument("post_type", type=str, help="The type of post to be made.")
    parser.add_argument(
        "soc", type=str, help="The social media platform (e.g., 'twitter', 'facebook')."
    )

    args = parser.parse_args()
    result = post_on_social(args.post_type, args.soc)
    print(result)
