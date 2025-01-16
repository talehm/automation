import csv
from typing import List
from .post_manager import PostManager


class LinkManager:
    """Manages link-related operations."""

    def __init__(self):
        self.post_manager = PostManager()

    def create_links(self, post_type: str) -> None:
        """Create links CSV file from posts."""
        posts = self.post_manager.fetch_paginated_posts(post_type)
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

        with open(csv_file, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=custom_headers, delimiter=";")
            writer.writeheader()

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
