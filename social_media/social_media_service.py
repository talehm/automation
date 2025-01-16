import random
import time
from typing import Optional
from enums import ExecutionStatus
from old_domain import posts_unused
from wordpress.post_manager import PostManager
from .storage import JsonFileStorage
from .message_generator import MessageGeneratorFactory
from .poster import SocialMediaPoster
from .config import SocialMediaConfigurations


class SocialMediaService:
    def __init__(self, social_platform: str):
        self.config = SocialMediaConfigurations.get_config_by_connection(
            social_platform
        )
        self.storage = JsonFileStorage(social_platform)
        self.message_generator = MessageGeneratorFactory.create_generator(
            social_platform
        )
        self.poster = SocialMediaPoster(self.config.id)

    def process_post(
        self, post_type: str, post_id: str, current_count: int
    ) -> ExecutionStatus:
        posted_ids = self.storage.load_posted_ids()
        if post_id in posted_ids:
            print(f"Post ID {post_id} already exists. Skipping...")
            return ExecutionStatus.ALREADY_EXISTS
        remaining_limit = self.config.limit - current_count
        if remaining_limit <= 0:
            print(f"Limit reached for {self.config.connection}. Skipping...")
            time.sleep(3)
            return ExecutionStatus.LIMIT_EXCEEDED
        post_manager = PostManager()
        item = post_manager.fetch_by_id(post_type, post_id)
        if item is None:
            return ExecutionStatus.FAILED
        message = self.message_generator.generate(item)
        self.poster.post(item, message)
        posted_ids.append(item["id"])
        self.storage.save_posted_ids(posted_ids)
        delay = random.randint(240, 480)
        time.sleep(delay)
        return ExecutionStatus.SUCCESS
