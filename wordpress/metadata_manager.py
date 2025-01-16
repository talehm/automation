from typing import Dict
from .post_manager import PostManager


class MetadataManager:
    """Manages post metadata operations."""

    def __init__(self):
        self.post_manager = PostManager()

    def update_metadata_all(self, post_type: str, params: Dict = None) -> None:
        """Update metadata for all posts of a specific type."""
        posts = self.post_manager.fetch_paginated_posts(post_type, params)
        start = len(posts)

        for post in posts[start - 1060 : start]:
            self.update_metadata(post_type, post)

    def update_metadata(self, post_type: str, item: Dict) -> None:
        """Update metadata for a single post."""
        data = {"meta": {"_yoast_wpseo_focuskw": "definition"}}
        self.post_manager.api_client.make_request(
            "POST", f"{post_type}/{item['id']}", data=data
        )
