import requests
from typing import Optional
from .config import DropboxConfig
from .interfaces import FileUploader, LinkGenerator, UrlFormatter


class DropboxUrlFormatter(UrlFormatter):
    """Handles formatting of Dropbox URLs to direct download links."""

    def format_url(self, url: str) -> str:
        """Format the shared link to a direct image URL."""
        direct_url = url.replace(
            "www.dropbox.com", "dl.dropboxusercontent.com"
        ).replace("?dl=0", "")
        return f"{direct_url.rstrip('/')}1"


class DropboxLinkGenerator(LinkGenerator):
    """Handles generation of Dropbox shared links."""

    def __init__(self, config: DropboxConfig, url_formatter: UrlFormatter):
        self.config = config
        self.url_formatter = url_formatter

    def create_link(self, file_path: str) -> Optional[str]:
        """Create a public shared link for the uploaded file."""
        headers = {
            "Authorization": f"Bearer {self.config.get_access_token()}",
            "Content-Type": "application/json",
        }

        payload = {
            "path": file_path,
            "settings": {"requested_visibility": "public"},
        }
        response = requests.post(
            self.config.SHARED_LINK_URL, headers=headers, json=payload
        )
        if response.status_code == 200:
            shared_link = response.json()["url"]
            return self.url_formatter.format_url(shared_link)

        print(f"Failed to create shared link: {response.status_code}, {response.text}")
        return None


class DropboxUploader(FileUploader):
    """Handles file uploads to Dropbox."""

    def __init__(self, config: DropboxConfig, link_generator: LinkGenerator):
        self.config = config
        self.link_generator = link_generator

    def upload(self, file_path: str, destination_path: str = None) -> Optional[str]:
        """Upload an image to Dropbox and return a public link."""
        if destination_path is None:
            destination_path = self.config.DEFAULT_UPLOAD_PATH
        headers = {
            "Authorization": f"Bearer {self.config.get_access_token()}",
            "Content-Type": "application/octet-stream",
            "Dropbox-API-Arg": f'{{"path": "{destination_path}", "mode": "add", "autorename": true, "mute": false}}',
        }
        try:
            with open(file_path, "rb") as image_file:
                response = requests.post(
                    self.config.UPLOAD_URL, headers=headers, data=image_file
                )
            if response.status_code == 200:
                uploaded_path = response.json()["path_display"]
                print("Image uploaded successfully!")
                return self.link_generator.create_link(uploaded_path)

            print(f"Failed to upload image: {response.status_code}, {response.text}")
            return None

        except Exception as e:
            print(f"Error uploading file: {str(e)}")
            return None
