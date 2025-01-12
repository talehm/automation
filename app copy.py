from flask import Flask, redirect, session, request, url_for
from pinterest.oauth import (
    get_pinterest_auth_url,
    exchange_code_for_token,
    refresh_access_token,
)
from pinterest.pin import (
    create_csv,
    get_pins,
    get_boards,
    create_pin,
    fetch_pins_from_board,
)
from utils import load_env_vars, save_tokens_to_env, get_env_var
from domain import posts
from image import dropbox, generator
import json
import os
import re
import time
from bs4 import BeautifulSoup
import random
from helpers import json_handler
import socials.social as social

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Load environment variables from .env file
load_env_vars()


def read_existing_ids(file_path):
    # Check if the file exists and is not empty
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, "r") as f:
            data = json.load(f)
            return {entry["id"] for entry in data}  # Return a set of IDs
    return set()  # Return an empty set if file doesn't exist or is empty


def read_page_value(file_path):
    # Check if the file exists
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            try:
                data = json.load(f)
                return data.get("page", None)  # Return the page value if it exists
            except json.JSONDecodeError:
                print("Error: Invalid JSON format.")
                return None
    else:
        print(f"Error: File {file_path} does not exist.")
        return None


def write_article_page(file_path, page_value):
    # If the file exists, update the page value
    if os.path.exists(file_path):
        with open(file_path, "r+") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}  # Start with an empty dict if JSON is invalid

            # Modify the page value
            data["page"] = page_value

            # Overwrite the file with the updated data
            f.seek(0)  # Move the cursor to the beginning of the file
            f.truncate()  # Clear the file before writing
            json.dump(data, f, indent=4)
    else:
        # Create a new file and write the initial page value
        with open(file_path, "w") as f:
            json.dump({"page": page_value}, f, indent=4)


# Function to write a new ID to the JSON file
def write_article_id(file_path, article_id):
    # Create the data structure if the file doesn't exist
    if os.path.exists(file_path):
        with open(file_path, "r+") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []  # Start with an empty list if JSON is invalid
            data.append({"id": article_id})
            f.seek(0)
            json.dump(data, f, indent=4)
    else:
        # Create a new file and write the first ID
        with open(file_path, "w") as f:
            json.dump([{"id": article_id}], f, indent=4)


@app.route("/token")
def token():
    auth_url = get_pinterest_auth_url()
    return redirect(auth_url)


@app.route("/house/<cat_id>")
def create_house(cat_id):
    session["access_token"] = get_env_var("ACCESS_TOKEN")
    json_file_path = "processes.json"
    board = get_boards("house")
    if board is None:
        return f"board {board} is not found. check get_bords method"
    # Optionally, create a pin using the access token
    existing_ids = read_existing_ids(json_file_path)

    page = 1
    while True:
        try:
            params = {"per_page": 100, "page": page}
            params["exclude"] = ",".join(map(str, existing_ids))
            articles = posts.fetch_by_category(cat_id)
            # print(articles)
            for article in articles:
                if article["id"] in existing_ids:
                    continue
                # upload image
                template_folder = (
                    "./image/templates/stories"  # Define your folder path here
                )
                img_local_url = generator.run(template_folder, article)
                imgur_url = dropbox.upload(img_local_url)
                print(imgur_url)

                article["pinterest_media"] = imgur_url
                html_description = article["excerpt"]["rendered"]
                soup = BeautifulSoup(html_description, "html.parser")
                description = soup.get_text()
                response = create_pin(
                    article,
                    description,
                    board["id"],
                )
                if response is True:
                    write_article_id(json_file_path, article["id"])
                delay = random.randint(60, 180)
                time.sleep(delay)
            page += 1
        except Exception as e:
            print(f"Unexpected error occurred: {e}")
            return []
    return "Finished!"


@app.route("/definitions/<lang>", methods=["GET"])
def create_definitions_hold(lang):
    if request.method != "GET":
        return "", 405  # Method not allowed
    post_type = "definition"
    session["access_token"] = get_env_var("ACCESS_TOKEN")
    json_file_path = "page.json"
    board = get_boards("definitions")
    if board is None:
        return f"board {board} is not found. check get_bords method"
    # Optionally, create a pin using the access token
    # existing_ids = read_existing_ids(json_file_path)
    section = next(
        (sec for sec in board["sections"] if sec["name"].lower() == str(lang).lower()),
        None,
    )
    try:
        definitions = json_handler.load_from_json("data/result.json")
        # datetime_strings = datetime.generate_datetime_strings(len(definitions), 0)
        template_folder = "./image/templates/" + board["name"]
        for index, definition in enumerate(definitions):
            if index >= 10:
                break
            item = posts.fetch_by_id(post_type, definition["id"])
            if item == None:
                continue
            content = item["content"]["rendered"]
            soup = BeautifulSoup(content, "html.parser")

            text = soup.get_text()
            text = re.sub(r"[“”]", '"', text)  # Replace double curly quotes
            # Replace invalid trailing character in URL
            text = re.sub(r"[″]", '"', text)
            # text = re.sub(r"[‘’]", '"', text)
            content = json.loads(text)

            result = random.choice(content["results"])
            img_local_url = generator.run(
                template_folder, item, None, "definition", result
            )
            imgur_url = dropbox.upload(img_local_url)
            if imgur_url is not None:
                item["pinterest_media"] = imgur_url
                word = content["word"]

                keywords = f"definition, meaning, english, vocabulary, {word}"
                # create_csv(
                #     item,
                #     result["definition"],
                #     board["name"],
                #     section["name"],
                #     datetime_strings[index],
                #     keywords,
                # )
                html_description = item["excerpt"]["rendered"]
                soup = BeautifulSoup(html_description, "html.parser")
                description = re.sub(r"[“”]", '"', soup.get_text())
                description = re.sub(r"[″]", '"', description)
                response = create_pin(item, description, board["id"])

                sleep_time = random.uniform(
                    10 * 60, 20 * 60
                )  # Convert minutes to seconds
                time.sleep(sleep_time)
            else:
                print("Token Expired")

    except Exception as e:
        print(f"Unexpected error occurred:{e}")
        return []
    return "Finished!"


@app.route("/pin/definitions/<lang>", methods=["GET"])
def create_pin_hold(lang):
    if request.method != "GET":
        return "", 405  # Method not allowed
    post_type = "definition"
    session["access_token"] = get_env_var("ACCESS_TOKEN")
    json_file_path = "page.json"
    board = get_boards("definitions")
    if board is None:
        return f"board {board} is not found. check get_bords method"
    # Optionally, create a pin using the access token
    # existing_ids = read_existing_ids(json_file_path)
    section = next(
        (sec for sec in board["sections"] if sec["name"].lower() == str(lang).lower()),
        None,
    )
    print(section)
    try:
        definitions = json_handler.load_from_json("data/result.json")
        # datetime_strings = datetime.generate_datetime_strings(len(definitions), 0)
        template_folder = "./image/templates/" + board["name"]
        for index, definition in enumerate(definitions):
            item = posts.fetch_by_id(post_type, definition["id"])
            print(1)
            content = item["content"]["rendered"]
            soup = BeautifulSoup(content, "html.parser")
            content = json.loads(soup.get_text())
            result = random.choice(content["results"])
            print(2)

            img_local_url = generator.run(
                template_folder, item, None, "definition", result
            )
            print(3)
            imgur_url = dropbox.upload(img_local_url)
            if imgur_url is not None:
                item["pinterest_media"] = imgur_url
                word = content["word"]
                keywords = f"definition, meaning, english, vocabulary, {word}"
                # create_csv(
                #     item,
                #     result["definition"],
                #     board["name"],
                #     section["name"],
                #     datetime_strings[index],
                #     keywords,
                # )
                html_description = item["excerpt"]["rendered"]
                soup = BeautifulSoup(html_description, "html.parser")
                description = soup.get_text()
                # response = create_pin(
                #     item,
                #     description,
                #     board["id"],
                # section["id"]
                # )
            else:
                print("Token Expired")

    except Exception as e:
        print(f"Unexpected error occurred:{e}")
        return []
    return "Finished!"


@app.route("/extract/definition/<lang>", methods=["GET"])
def create_definitions(lang):
    if request.method != "GET":
        return "", 405  # Method not allowed
    post_type = "definition"
    session["access_token"] = get_env_var("ACCESS_TOKEN")

    board = get_boards("definitions")
    if board is None:
        return f"board {board} is not found. check get_bords method"
    section = next(
        (sec for sec in board["sections"] if sec["name"].lower() == str(lang).lower()),
        None,
    )
    fetch_pins_from_board(board["id"], section["id"])
    posts.fetch_pins(post_type)
    json_handler.filter_by_title(
        "data/pins.json", "data/definitions.json", "data/result.json"
    )
    # Optionally, create a pin using the access token
    # existing_ids = read_existing_ids(json_file_path)
    return "True"


@app.route("/riddle", methods=["GET"])
def create_puzzles():
    if request.method != "GET":
        return "", 405  # Method not allowed
    post_type = "riddle"
    # session["access_token"] = get_env_var("ACCESS_TOKEN")
    # board = get_boards("puzzles")
    # if board is None:
    #     return f"board {board} is not found. check get_bords method"
    # # Optionally, create a pin using the access token
    # # existing_ids = read_existing_ids(json_file_path)
    # section = next(
    #     (sec for sec in board["sections"] if sec["name"].lower() == str(lang).lower()),
    #     None,
    # )
    try:
        riddles = json_handler.load_from_json("data/riddles.json")
        # datetime_strings = datetime.generate_datetime_strings(len(riddles), 0)
        template_folder = "./image/templates/riddles"
        # board["name"]
        number = 1
        riddles_100 = [
            item
            for index, item in enumerate(riddles)
            if (number - 1) * 20 <= index < number * 20
        ]
        number_of_riddles_per_article = 20
        total_riddles = len(riddles)

        # Iterate over the riddles in chunks of 20
        for number in range(1, (total_riddles // number_of_riddles_per_article) + 2):
            riddles_chunk = [
                item
                for index, item in enumerate(riddles)
                if (number - 1) * number_of_riddles_per_article
                <= index
                < number * number_of_riddles_per_article
            ]

            item = posts.create_post(post_type, riddles_chunk, number)
        # for index, item in enumerate(riddles_100):

        # item = posts.fetch_by_id(post_type, definition["id"])
        # read content from json
        # if index == 0:
        #     riddle = item["riddle"]
        #     answer = item["answer"]

        # posts.update_metadata(post_type, item)
        # soup = BeautifulSoup(content, "html.parser")
        # content = json.loads(soup.get_text())
        # result = random.choice(content["results"])
        # img_local_url = generator.run(template_folder, item, None, "riddle")
        # time.sleep(3)
        # imgur_url = dropbox.upload(img_local_url)
        # if imgur_url is not None:
        #     item["pinterest_media"] = imgur_url
        #     word = content["word"]
        #     keywords = (
        #         f"puzzle games, logic puzzles, Funny Quotes, brain, brain break"
        #     )
        #     create_csv(
        #         item,
        #         item["riddle"],
        #         board["name"],
        #         publish_date=datetime_strings[index],
        #         keywords=keywords,
        #     )
        # else:
        #     print("Token Expired")

    except Exception as e:
        print(f"Unexpected error occurred:{e}")
        return []
    return "Finished!"


@app.route("/create/<board>/<cat_id>")
def create(board, cat_id):
    session["access_token"] = get_env_var("ACCESS_TOKEN")
    json_file_path = "processes.json"
    board = get_boards(board)
    # Optionally, create a pin using the access token
    existing_ids = read_existing_ids(json_file_path)
    section = next(
        (sec for sec in board["sections"] if sec["cat_id"] == int(cat_id)),
        None,
    )

    articles = posts.fetch_by_category(cat_id)
    for article in articles:
        if article["id"] in existing_ids:
            continue

        # upload image
        template_folder = (
            "./image/templates/" + board["name"]
        )  # Define your folder path here
        img_local_url = generator.run(template_folder, article)
        imgur_url = dropbox.upload(img_local_url)
        # print(imgur_url)

        article["pinterest_media"] = imgur_url
        html_description = article["excerpt"]["rendered"]
        soup = BeautifulSoup(html_description, "html.parser")
        description = soup.get_text()
        response = createe_pin(article, description, board["id"], section["id"])
        if response is True:
            write_article_id(json_file_path, article["id"])
        time.sleep(10)
    response = get_pins()
    return "Finished!"


@app.route("/social/<post_type>/<soc>", methods=["GET"])
def post_on_social(post_type, soc):
    definitions = json_handler.load_from_json("data/definitions.json")
    ids = json_handler.load_from_json(f"socials/{soc}_ids.json")
    count = 1
    for index, definition in enumerate(definitions):
        if definition["id"] not in ids:
            social.run(post_type, definition["id"], soc, count)
            count += 1
    return "Stopped"


@app.route("/")
def login():
    return [
        {
            "name": "stories",
            "id": "882283451939745557",
            "sections": [
                {"id": "5398508827117151890", "name": "true", "cat_id": 5},
                {
                    "id": "5398508804082025745",
                    "name": "bedtime",
                    "cat_id": 1,
                },
                {"id": "5398508424346526516", "name": "horror", "cat_id": 23},
                {"id": "5398509851036923141", "name": "mystery", "cat_id": 7},
            ],
        },
    ]
    # return "Running!"


# UNCOMMENT WHEN TOKEN EXPIREs
# Redirect to Pinterest for OAuth authorization
# auth_url = get_pinterest_auth_url()
# return redirect(auth_url)


@app.route("/definition/meta")
def update_metadata():
    posts.update_metadata_all("definition")
    return "Done"


@app.route("/definition/links")
def create_links():
    posts.create_links("definition")
    return "Done"


@app.route("/callback")
def callback():
    # Handle Pinterest OAuth callback and token exchange
    code = request.args.get("code")
    if not code:
        return "Error: No authorization code provided."

    tokens = exchange_code_for_token(code)
    if tokens:
        save_tokens_to_env(tokens)  # Save access and refresh tokens to .env
        session["access_token"] = tokens["access_token"]
        json_file_path = "processes.json"

        # # Optionally, create a pin using the access token
        # existing_ids = read_existing_ids(json_file_path)

        # articles = posts.fetch_all()
        # for article in articles:
        #     if article["id"] in existing_ids:
        #         continue
        #     # upload image

        #     template_folder = (
        #         "./image/templates/vintage"  # Define your folder path here
        #     )
        # img_local_url = generator.run(template_folder, article)
        # imgur_url = dropbox.upload(img_local_url)
        # print(imgur_url)

        # article["pinterest_media"] = imgur_url
        # response = create_pin(article)
        # if response is True:
        #     write_article_id(json_file_path, article["id"])
        # response = get_pins()
        # print(response)
        return tokens
    else:
        return "Error: Failed to get access token."


@app.route("/refresh")
def refresh():
    # Manually refresh access token if needed
    new_access_token = refresh_access_token()
    return f"New Access Token: {new_access_token}"


if __name__ == "__main__":
    WP_URL = get_env_var("WP_URL")
    app.run(port=8000, debug=False)
