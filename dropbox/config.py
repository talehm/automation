from dataclasses import dataclass
from utils.env_manager import EnvManager


@dataclass
class DropboxConfig:
    """Configuration class for Dropbox API endpoints and settings."""

    UPLOAD_URL: str = "https://content.dropboxapi.com/2/files/upload"
    SHARED_LINK_URL: str = (
        "https://api.dropboxapi.com/2/sharing/create_shared_link_with_settings"
    )
    DEFAULT_UPLOAD_PATH: str = "/pinterest/image.jpg"

    @staticmethod
    def get_access_token() -> str:
        """Fetch the Dropbox access token from environment variables."""
        return EnvManager.get_env_var("DROPBOX_TOKEN")
