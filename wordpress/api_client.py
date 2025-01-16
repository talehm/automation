import requests
import json
from requests.auth import HTTPBasicAuth
from .config import WordPressConfig


class WordPressApiClient:
    """Handles API communication with WordPress."""

    def __init__(self):
        self.config = WordPressConfig()
        self.config.initialize()

    def make_request(
        self, method: str, endpoint: str, params=None, data=None, base_route="wp/v2"
    ):
        """Make an HTTP request to the WordPress API."""
        url = f"{self.config.get_base_url()}/{base_route.strip()}/{endpoint.strip()}"
        credentials = self.config.get_credentials()

        try:
            response = requests.request(
                method,
                url,
                headers=self.config.get_headers(),
                params=params,
                data=json.dumps(data) if data else None,
                auth=HTTPBasicAuth(credentials["username"], credentials["password"]),
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request error ({method} {url}): {e}")
            return None

    def get_max_page(self, post_type: str, params: dict) -> int:
        """Get the maximum number of pages for pagination."""
        response = requests.get(
            f"{self.config.get_base_url()}/wp/v2/{post_type}",
            headers=self.config.get_headers(),
            params=params,
        )
        if response.status_code == 200:
            return int(response.headers.get("X-WP-TotalPages", 1))
        return 1
