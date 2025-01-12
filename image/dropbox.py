# dropbox.py

import requests
from utils import get_env_var

# Constants for Dropbox API endpoints
UPLOAD_URL = "https://content.dropboxapi.com/2/files/upload"
SHARED_LINK_URL = (
    "https://api.dropboxapi.com/2/sharing/create_shared_link_with_settings"
)


def get_access_token():
    """Fetch the Dropbox access token from environment variables."""
    return get_env_var("DROPBOX_TOKEN")


def upload_image(file_path, dropbox_path="/pinterest/image.jpg"):
    """Upload an image to Dropbox and return a public link to the uploaded image."""
    access_token = get_access_token()

    upload_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/octet-stream",
        "Dropbox-API-Arg": f'{{"path": "{dropbox_path}", "mode": "add", "autorename": true, "mute": false}}',
    }

    # Open and upload the image file
    with open(file_path, "rb") as image_file:
        upload_response = requests.post(
            UPLOAD_URL, headers=upload_headers, data=image_file
        )

    if upload_response.status_code == 200:
        uploaded_file_path = upload_response.json()["path_display"]
        print("Image uploaded successfully!")

        # Create shared link for the uploaded file
        return create_shared_link(uploaded_file_path, access_token)
    else:
        print(
            f"Failed to upload image: {upload_response.status_code}, {upload_response.text}"
        )
        return None


def create_shared_link(file_path, access_token):
    """Create a public shared link for the uploaded file."""
    shared_link_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    shared_link_payload = {
        "path": file_path,
        "settings": {"requested_visibility": "public"},  # Can be adjusted as needed
    }

    # Request to create the shared link
    shared_link_response = requests.post(
        SHARED_LINK_URL, headers=shared_link_headers, json=shared_link_payload
    )

    if shared_link_response.status_code == 200:
        shared_link = shared_link_response.json()["url"]
        return format_direct_image_url(shared_link)
    else:
        print(
            f"Failed to create shared link: {shared_link_response.status_code}, {shared_link_response.text}"
        )
        return None


def format_direct_image_url(shared_link):
    """Format the shared link to a direct image URL."""
    direct_image_url = shared_link.replace(
        "www.dropbox.com", "dl.dropboxusercontent.com"
    ).replace("?dl=0", "")
    # Ensure the URL is a direct image link
    return direct_image_url.rstrip("/") + "1"


if __name__ == "__main__":
    # Example usage of the upload functionality
    image_path = "element_image.png"  # Replace with the actual path
    direct_image_url = upload_image(image_path)

    if direct_image_url:
        print("Direct Image URL:", direct_image_url)
