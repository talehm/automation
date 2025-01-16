import argparse
import sys
import os
import time

current_dir = os.path.dirname(__file__)
# Move one folder up
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(parent_dir)
from enums import ExecutionStatus
import social_media

# from socials import social
from utils.file_handler import JsonFileHandler
import random


def post_on_social(post_type, soc):
    data_file_path = os.path.join(parent_dir, "data", "definitions.json")
    logs_file_path = os.path.join(parent_dir, "social_media/data", f"{soc}_ids.json")
    definitions = JsonFileHandler(data_file_path).read()
    ids = JsonFileHandler(logs_file_path).read()

    count = 1
    for definition in definitions:
        if definition["id"] not in ids:
            status = social_media.run(post_type, definition["id"], soc, count)
            if status == ExecutionStatus.SUCCESS:
                print(f"created: {definition["id"]} : {definition["title"]}")
                count += 1
    return "Stopped"


if __name__ == "__main__":
    # Generate a random sleep duration between 180 and 240 seconds (3 to 4 minutes)
    # random_sleep = random.randint(60, 240)

    # time.sleep(random_sleep)
    parser = argparse.ArgumentParser(
        description="Post on social media using definitions and IDs."
    )
    parser.add_argument("post_type", type=str, help="The type of post to be made.")
    parser.add_argument(
        "soc", type=str, help="The social media platform (e.g., 'twitter', 'facebook')."
    )

    args = parser.parse_args()
    result = post_on_social(args.post_type, args.soc)
