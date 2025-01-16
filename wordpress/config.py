from utils.env_manager import EnvManager


class WordPressConfig:
    """Configuration class for WordPress API settings."""

    @staticmethod
    def initialize():
        EnvManager.load_env_vars()

    @staticmethod
    def get_base_url():
        return EnvManager.get_env_var("WP_URL")

    @staticmethod
    def get_credentials():
        return {
            "username": EnvManager.get_env_var("WP_USERNAME"),
            "password": EnvManager.get_env_var("WP_PASSWORD"),
            "auth": EnvManager.get_env_var("WP_AUTH"),
        }

    @staticmethod
    def get_headers():
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36",
        }
