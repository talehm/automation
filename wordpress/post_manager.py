from typing import List, Dict, Optional
from .api_client import WordPressApiClient
from helpers import riddle_handler
from utils.file_handler import JsonFileHandler


class PostManager:
    """Manages WordPress post operations."""

    def __init__(self):
        self.api_client = WordPressApiClient()

    def create_post(
        self, type: str, item: dict, number: int, status: str = "publish"
    ) -> Optional[dict]:
        """Create a new WordPress post."""
        post_data = riddle_handler.prepare(type, item, number)
        response = self.api_client.make_request("POST", "riddle", data=post_data)

        if response:
            print("Post created successfully! ID:", response.get("id"))
            return response
        print("Failed to create post.")
        return None

    def fetch_paginated_posts(
        self,
        post_type: str,
        params: Optional[dict] = None,
        max_page: Optional[int] = None,
    ) -> List[dict]:
        """Fetch posts with pagination."""
        params = params or {"per_page": 100}
        if max_page is None:
            max_page = self.api_client.get_max_page(post_type, params)

        all_data = []
        for page in range(1, max_page + 1):
            params["page"] = page
            data = self.api_client.make_request("GET", post_type, params=params)
            if data:
                all_data.extend(data)
        return all_data

    def fetch_featured_media(self, media_id: int) -> Optional[dict]:
        """Fetch featured media for a post."""
        if media_id:
            return self.api_client.make_request("GET", f"media/{media_id}")
        print("No featured media found.")
        return None

    # Fetch pins from WordPress
    def fetch_pins(self, post_type):
        data = self.fetch_paginated_posts(post_type)
        pins = [
            {"id": post["id"], "title": post["title"]["rendered"], "link": post["link"]}
            for post in data
        ]
        file_handler = JsonFileHandler("data/definitions.json")
        file_handler.write(pins)
        return pins

    # Fetch single post by ID
    def fetch_by_id(self, post_type, post_id):
        post = self.api_client.make_request("GET", f"{post_type}/{post_id}")
        if post:
            media = self.fetch_featured_media(post.get("featured_media"))
            if media:
                post["media"] = media
        return post
