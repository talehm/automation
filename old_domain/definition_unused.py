import requests
import json
from requests.auth import HTTPBasicAuth
from utils import get_env_var
from utils.env_manager import EnvManager


# Create a post on WordPress
def create(title, content, status="publish"):
    WP_URL = get_env_var("WP_URL")
    USERNAME = get_env_var("USERNAME")
    PASSWORD = get_env_var("PASSWORD")
    url = f"{WP_URL}/definition"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    # Data for creating a post
    post_data = {"title": title, "content": content, "status": status}

    try:
        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(post_data),
            auth=HTTPBasicAuth(USERNAME, PASSWORD),
        )
        if response.status_code == 201:
            print("Post created successfully!")
            print("Post ID:", response.json()["id"])
        else:
            print(f"Failed to create post: {response.status_code}")
            print("Response:", response.text)
    except Exception as e:
        print(f"Error occurred: {e}")


# Call the function with a specific post ID
# fetch_post_with_featured_media(123)  # Replace 123 with the actual post ID
