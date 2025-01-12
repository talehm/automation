import requests
from utils import get_env_var


def upload(image_path):
    client_id = get_env_var("IMGUR_CLIENT_ID")
    headers = {
        "Authorization": f"Client-ID {client_id}",
    }

    with open(image_path, "rb") as image_file:
        response = requests.post(
            "https://api.imgur.com/3/image",
            headers=headers,
            files={"image": image_file},
        )

    # Check if the upload was successful
    if response.status_code == 200:
        image_url = response.json()["data"]["link"]
        return image_url
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")
