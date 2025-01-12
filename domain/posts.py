import requests
import json
from requests.auth import HTTPBasicAuth
from utils import get_env_var
from helpers import post_handler
import utils
import re
import csv

# Global variables
WP_URL = get_env_var("WP_URL")
USERNAME = get_env_var("WP_USERNAME")
PASSWORD = get_env_var("WP_PASSWORD")
AUTH = get_env_var("WP_AUTH")
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36",
}


def make_request(method, endpoint, params=None, data=None, base_route="wp/v2"):
    """
    Helper function to handle API requests.
    """
    # Clean the URL components to remove leading/trailing whitespaces and newlines
    wp = WP_URL
    base_route = base_route.strip()
    endpoint = endpoint.strip()
    USERNAME = USERNAME
    PASSWORD = PASSWORD
    url = f"{wp}/{base_route}/{endpoint}"
    print(url)
    # if method == "POST":
    #     HEADERS["Authorization"] = f"Basic {AUTH}"
    try:
        response = requests.request(
            method,
            url,
            headers=HEADERS,
            params=params,
            data=json.dumps(data) if data else None,
            auth=HTTPBasicAuth(USERNAME, PASSWORD),
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request error ({method} {url}): {e}")
        return None


# Create a post on WordPress
def create_post(type, item, number, status="publish"):
    post_data = post_handler.prepare(type, item, number)
    response = make_request("POST", "riddle", data=post_data)

    if response:
        print("Post created successfully! ID:", response.get("id"))
        return response
    else:
        print("Failed to create post.")


# Fetch maximum page count
def get_max_page(post_type, params):
    response = requests.get(
        f"{WP_URL}/wp/v2/{post_type}", headers=HEADERS, params=params
    )
    if response.status_code == 200:
        return int(response.headers.get("X-WP-TotalPages", 1))
    print(f"{WP_URL}/wp/v2/{post_type}")
    return 1


# Fetch posts with pagination
def fetch_paginated_posts(post_type, params=None, max_page=None):
    print(max_page)

    params = params or {"per_page": 100}
    if max_page == None:
        max_page = get_max_page(post_type, params)
    all_data = []
    for page in range(1, max_page + 1):
        params["page"] = page
        data = make_request("GET", post_type, params=params)
        if data:
            all_data.extend(data)
    return all_data


def create_links(post_type):
    posts = fetch_paginated_posts(post_type)
    # Define CSV file path
    csv_file = "data/links.csv"
    custom_headers = [
        "ID",
        "Type",
        "Keywords (ILJ)",
        "Title",
        "Url",
        "Sub-Type",
        "Outgoing",
        "Incoming",
    ]

    # Writing to CSV file with post ID
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "ID",
                "Type",
                "Keywords (ILJ)",
                "Title",
                "Url",
                "Sub-Type",
                "Outgoing",
                "Incoming",
            ],
            delimiter=";",
        )

        # Write custom headers
        writer.writeheader()

        # Write rows of data, but map the data to custom headers
        for post in posts:
            word = post["title"]["rendered"].replace("Definition of ", "")
            writer.writerow(
                {
                    "ID": post["id"],
                    "Type": "post",
                    "Keywords (ILJ)": word,
                    "Title": post["title"]["rendered"],
                    "Url": post["link"],
                    "Sub-Type": post["type"],
                    "Incoming": 0,
                    "Outgoing": 0,
                }
            )


# Fetch posts by category
def fetch_by_category(cat_id):
    posts = make_request("GET", f"posts?categories={cat_id}")
    if posts:
        for post in posts:
            media = fetch_featured_media(post.get("featured_media"))
            if media:
                post["media"] = media
        return posts
    return []


# Fetch single post by ID
def fetch_by_id(post_type, post_id):
    post = make_request("GET", f"{post_type}/{post_id}")
    if post:
        media = fetch_featured_media(post.get("featured_media"))
        if media:
            post["media"] = media
    return post


# Fetch all posts
def fetch_all_posts():
    posts = fetch_paginated_posts("posts")
    for post in posts:
        media = fetch_featured_media(post.get("featured_media"))
        if media:
            post["media"] = media
    return posts


# Fetch definitions


def fetch_definitions(post_type, params=None):
    posts = fetch_paginated_posts(post_type, params)
    return [{"id": post["id"], "title": post["title"]["rendered"]} for post in posts]


# Fetch featured media
def fetch_featured_media(media_id):
    if media_id:
        return make_request("GET", f"media/{media_id}")
    print("No featured media found.")
    return None


# Fetch pins from WordPress
def fetch_pins(post_type):
    data = fetch_paginated_posts(post_type)
    pins = [
        {"id": post["id"], "title": post["title"]["rendered"], "link": post["link"]}
        for post in data
    ]
    utils.save_to_json("data/definitions.json", pins)
    return pins


def update_metadata_all(post_type, params=None):
    posts = fetch_paginated_posts(post_type, params)
    start = len(posts)
    for index, post in enumerate(posts[start - 1060 : start]):
        data = {
            "meta": {
                "_yoast_wpseo_focuskw": "definition"
            }  # Replace with your focus keyword
        }
        make_request("POST", f"definition/{post['id']}", data=data)


def update_metadata(post_type, item):
    data = {
        "meta": {
            "_yoast_wpseo_focuskw": "definition"  # Replace with your focus keyword
        }
    }
    # Replace with your focus keyword
    make_request("POST", f"{post_type}/{item['id']}", data=data)
