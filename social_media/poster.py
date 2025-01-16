from typing import Dict, List
from .config import SocialMediaConfigurations
from wordpress.api_client import WordPressApiClient


class SocialMediaPoster:
    def __init__(self, connection_id: str):
        self.connection_id = connection_id
        self.config = SocialMediaConfigurations.get_config_by_id(connection_id)
        self.api_client = WordPressApiClient()

    def post(self, item: Dict, message: str) -> Dict:
        skipped_connections = [
            s.id
            for s in SocialMediaConfigurations.SOCIAL_CONFIG
            if s.id != self.connection_id
        ]
        payload = {
            "message": message,
            "skipped_connections": skipped_connections,
            "async": True,
            "featured_image": "dfd",
        }
        response = self.api_client.make_request(
            "POST",
            f"publicize/{item['id']}?_locale=user",
            data=payload,
            base_route="jetpack/v4",
        )
        return response
