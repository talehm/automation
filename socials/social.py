import json
import time
import random
import requests
from domain import posts

# API configuration
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Basic xxxx",
}

# Social media config
SOCIAL_CONFIG = [
    {"connection": "instagram", "id": "25490838", "limit": 50},
    {"connection": "facebook", "id": "25490839", "limit": 35},
    {"connection": "bluesky", "id": "25490844", "limit": 100},
    {"connection": "tumblr", "id": "25491586", "limit": 250},
    {"connection": "threads", "id": "25491600", "limit": 20},
]


# Function to load posted IDs
def load_posted_ids(file_name):
    try:
        with open(file_name, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


# Function to save posted IDs
def save_posted_ids(file_name, data):
    with open(file_name, "w") as file:
        json.dump(data, file)


def generate_message(item, social):
    message = ""
    if item["type"] == "definition":
        brief = ""
        if item["acf"]["brief"] != None:
            brief = json.loads(item["acf"]["brief"])

        word = item["title"]["rendered"].replace("Definition of ", "")
        if social == "bluesky":
            message = (
                word
                + "\n- "
                + brief[0].capitalize()
                + "\n\n"
                + f"Learn More... \n\n\n#definition #{word.replace(' ', '')} #meaning #english #ielts"
            )
        if social == "facebook":
            message = (
                word
                + "\n- "
                + brief[0].capitalize()
                + "\n\n"
                + f"Learn More... \n\n\n#definition #{word.replace(' ', '')} #meaning #english #ielts"
            )
        if social == "tumblr":
            message = (
                word
                + "\n- "
                + brief[0].capitalize()
                + "\n\n"
                + f"Learn More... \n\n\n#definition #{word.replace(' ', '')} #meaning #english #ielts"
            )
        if social == "threads":
            message = (
                "https://www.pngall.com/wp-content/uploads/8/Sample.png"
                + word
                + "\n- "
                + brief[0].capitalize()
                + "\n\n"
                + f"Learn More... \n\n\n #{word.replace(' ', '')} "
            )
    return message


def post(item, connection_id):
    skipped_connections = [s["id"] for s in SOCIAL_CONFIG if s["id"] != connection_id]
    social = [s for s in SOCIAL_CONFIG if s["id"] == connection_id][0]
    message = generate_message(item, social["connection"])
    payload = {
        "message": message,
        "skipped_connections": skipped_connections,
        "async": True,
        "featured_image": "dfd",
    }
    # API_URL = f"https://trueandfiction.com/wp-json/jetpack/v4/publicize/{item['id']}?_locale=user"
    response = posts.make_request(
        "POST",
        f"publicize/{item['id']}?_locale=user",
        data=payload,
        base_route="jetpack/v4",
    )
    # response = requests.post(API_URL, headers=HEADERS, json=payload)
    return response


# Function to post to API
def run(post_type, post_id, soc, count):
    connection = [social for social in SOCIAL_CONFIG if social["connection"] == soc][0]
    connection_id = connection["id"]
    limit = connection["limit"]
    file_name = f"socials/{soc}_ids.json"
    posted_ids = load_posted_ids(file_name)
    # Skip already posted social IDs
    if post_id in posted_ids:
        print(f"Post ID {post_id} already exists. Skipping...")
        return  # You can return here to skip processing this post
    # Check how many more posts can be made
    else:
        item = posts.fetch_by_id(post_type, post_id)
        remaining_limit = limit - count
        if remaining_limit <= 0:
            print(f"Limit reached for {connection}. Skipping...")
            time.sleep(3)
        else:
            if item == None:
                return
            # Message to be posted
            response = post(item, connection_id)
            posted_ids.append(item["id"])
            save_posted_ids(file_name, posted_ids)
            delay = random.randint(1200, 1800)
            time.sleep(delay)


# # Process each social connection
# for social in SOCIAL_CONFIG:
#     connection = social["connection"]
#     connection_id = social["id"]
#     limit = social["limit"]

#     # File to store posted IDs for this connection
#     file_name = f"{connection}_posted_ids.json"
#     posted_ids = load_posted_ids(file_name)

#     # Skip already posted social IDs
#     skipped_connections = [s["id"] for s in SOCIAL_CONFIG if s["id"] != connection_id]

#     # Check how many more posts can be made
#     remaining_limit = limit - len(posted_ids)
#     if remaining_limit <= 0:
#         print(f"Limit reached for {connection}. Skipping...")
#         continue

#     # Post until the limit is reached
#     for _ in range(remaining_limit):
#         response = post_to_social(connection_id, skipped_connections)
#         if response.status_code == 200:
#             print(f"Posted successfully on {connection}")
#             posted_ids.append(len(posted_ids) + 1)
#             save_posted_ids(file_name, posted_ids)
#         else:
#             print(f"Failed to post on {connection}: {response.status_code}")

#         # Random sleep between 20–30 minutes
#         sleep_time = random.uniform(20 * 60, 30 * 60)
#         print(f"Sleeping for {sleep_time / 60:.2f} minutes...")
#         time.sleep(sleep_time)
