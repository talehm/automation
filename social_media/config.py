from dataclasses import dataclass
from typing import List


@dataclass
class SocialMediaConfig:
    connection: str
    id: str
    limit: int


class SocialMediaConfigurations:
    HEADERS = {
        "Content-Type": "application/json",
        "Authorization": "Basic xxxx",
    }
    SOCIAL_CONFIG: List[SocialMediaConfig] = [
        SocialMediaConfig("instagram", "25490838", 50),
        SocialMediaConfig("facebook", "25490839", 35),
        SocialMediaConfig("bluesky", "25490844", 100),
        SocialMediaConfig("tumblr", "25491586", 250),
        SocialMediaConfig("threads", "25491600", 20),
    ]

    @classmethod
    def get_config_by_connection(cls, connection: str) -> SocialMediaConfig:
        return next(
            (config for config in cls.SOCIAL_CONFIG if config.connection == connection),
            None,
        )

    @classmethod
    def get_config_by_id(cls, connection_id: str) -> SocialMediaConfig:
        return next(
            (config for config in cls.SOCIAL_CONFIG if config.id == connection_id), None
        )
