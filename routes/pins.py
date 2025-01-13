from db.pinterest import PinterestLinkDatabase
from flask import Blueprint, session, request
from services.pin_service import PinService
from services.board_service import BoardService
from services.csv_service import CSVService

from image import generator
from helpers import datetime

# from services.image_service import generate_and_upload_image
from utils import read_existing_ids, write_article_id, fromHtml
from bs4 import BeautifulSoup
from image import dropbox
import utils
from domain import posts
import time
import random
import re
import json

pins_bp = Blueprint("pins", __name__)
pin_service = PinService()
board_service = BoardService()
csv_service = CSVService()


@pins_bp.route("/house/<cat_id>")
def create_house(cat_id):
    session["access_token"] = utils.get_env_var("ACCESS_TOKEN")
    json_file_path = "processes.json"
    board = board_service.get_boards("house")

    if board is None:
        return f"board {board} is not found. check get_boards method"

    existing_ids = read_existing_ids(json_file_path)

    try:
        params = {"per_page": 100, "exclude": ",".join(map(str, existing_ids))}
        articles = posts.fetch_by_category(cat_id)

        for article in articles:
            if article["id"] in existing_ids:
                continue

            img_local_url = generator.run("stories", article)

            if not img_local_url:
                continue

            imgur_url = dropbox.upload_image(img_local_url)

            article["pinterest_media"] = imgur_url
            html_description = article["excerpt"]["rendered"]
            description = BeautifulSoup(html_description, "html.parser").get_text()

            if pin_service.create_pin(article, description, board["id"]):
                write_article_id(json_file_path, article["id"])
            # print(article)
            delay = random.randint(60, 180)
            time.sleep(delay)

    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        return e

    return "Finished!"


@pins_bp.route("/create/<board>/<cat_id>")
def create(board, cat_id):
    session["access_token"] = utils.get_env_var("ACCESS_TOKEN")
    json_file_path = "processes.json"
    board = board_service.get_boards(board)
    existing_ids = read_existing_ids(json_file_path)
    section = next(
        (sec for sec in board["sections"] if sec["cat_id"] == int(cat_id)),
        None,
    )
    articles = posts.fetch_by_category(cat_id)
    for article in articles:
        if article["id"] in existing_ids:
            continue
        template_folder = f"./image/templates/{board['name']}"
        img_local_url = generator.run(template_folder, article)
        imgur_url = dropbox.upload_image(img_local_url)
        article["pinterest_media"] = imgur_url
        description = article["excerpt"]["rendered"]
        response = pin_service.create_pin(
            article, description, board["id"], section["id"]
        )
        if response is True:
            write_article_id(json_file_path, article["id"])
        time.sleep(10)
    return "Finished!"


@pins_bp.route("/definition/<mode>", methods=["GET"])
@pins_bp.route("/definition", methods=["GET"])
def create_definitions_hold(mode=None):
    if request.method != "GET":
        return "", 405  # Method not allowed
    post_type = "definition"
    session["access_token"] = utils.get_env_var("ACCESS_TOKEN")
    json_file_path = "page.json"
    board = board_service.get_boards("definitions")
    if board is None:
        return f"board {board} is not found. Check the get_boards method."

    # section = next(
    #     (sec for sec in board["sections"] if sec["name"].lower() == str(lang).lower()),
    #     None,
    # )

    try:
        definitions = utils.load_from_json("data/result.json")
        template_folder = f"./image/templates/{board['name']}"
        for index, definition in enumerate(definitions):
            if mode != "db" and index >= 10:
                break
            is_created_on_db = False
            if mode == "db":
                db = PinterestLinkDatabase()
                is_created_on_db = db.exists(definition["id"])
                if is_created_on_db:
                    continue
            item = posts.fetch_by_id(post_type, definition["id"])
            if item is None:
                continue

            content = fromHtml(item["content"]["rendered"])
            content = json.loads(content)

            result = random.choice(content["results"])
            img_local_url = generator.run(
                template_folder, item, None, "definition", result
            )
            imgur_url = dropbox.upload_image(img_local_url)
            if imgur_url is not None:
                item["pinterest_media"] = imgur_url
                word = content["word"]

                if mode == "db" and is_created_on_db == False:
                    content = fromHtml(item["excerpt"]["rendered"])
                    if db is None:
                        db = PinterestLinkDatabase()
                    keywords = f"definition, meaning, english, vocabulary, {word}"
                    # Sample data to insert
                    title = item["title"]["rendered"]
                    description = content
                    media_url = imgur_url
                    board_id = board["id"]
                    board_section_id = None
                    alt_text = title
                    keywords = keywords
                    link = item["link"]
                    post_id = item["id"]

                    # Insert the data into the pinterest_link table
                    db.insert_pinterest_link(
                        post_id,
                        link,
                        title,
                        description,
                        media_url,
                        board_id,
                        board_section_id,
                        alt_text,
                        keywords,
                    )

                    # Close the database connection
                    db.close()
                elif mode == "csv":
                    keywords = f"definition, meaning, english, vocabulary, {word}"
                    datetime_strings = datetime.generate_datetime_strings(
                        len(definitions), 0
                    )

                    csv_service.create_csv(
                        item,
                        result["definition"],
                        board["name"],
                        None,
                        datetime_strings[index],
                        keywords,
                    )
                else:
                    content = fromHtml(item["excerpt"]["rendered"])
                    pin_service.create_pin(item, content, board["id"])

                    # sleep_time = random.uniform(10 * 60, 20 * 60)  # 10 to 20 minutes
                    # time.sleep(sleep_time)
            else:
                print("Token Expired")
                break

    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        return []
    return "Finished!"


@pins_bp.route("/extract/definition/", methods=["GET"])
def create_definitions():
    if request.method != "GET":
        return "", 405  # Method not allowed
    post_type = "definition"
    session["access_token"] = utils.get_env_var("ACCESS_TOKEN")
    board = board_service.get_boards("definitions")
    if board is None:
        return f"board {board} is not found."
    # section = next(
    #     (sec for sec in board["sections"] if sec["name"].lower() == str(lang).lower()),
    #     None,
    # )
    pin_service.fetch_pins_from_board(board["id"])
    posts.fetch_pins(post_type)
    utils.filter_by_title("data/pins.json", "data/definitions.json", "data/result.json")
    return "True"
