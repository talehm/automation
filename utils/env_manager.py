import os
from dotenv import load_dotenv
from typing import Dict, Optional


class EnvManager:
    """Handles all environment variable related operations."""

    @staticmethod
    def load_env_vars() -> None:
        dotenv_path = os.path.join(os.path.dirname(__file__), "", ".env")
        print(dotenv_path)
        load_dotenv(dotenv_path)

    @staticmethod
    def save_tokens(tokens: Dict[str, str]) -> None:
        load_dotenv()

        env_vars = {
            "ACCESS_TOKEN": tokens["access_token"],
            "REFRESH_TOKEN": tokens["refresh_token"],
            "EXPIRES_IN": str(tokens["expires_in"]),
        }
        try:
            with open(".env", "r") as f:
                lines = f.readlines()
        except FileNotFoundError:
            lines = []
        updated_lines = []
        for line in lines:
            key = line.split("=")[0].strip()
            if key in env_vars:
                updated_lines.append(f"{key}={env_vars[key]}\n")
                env_vars.pop(key)
            else:
                updated_lines.append(line)
        for key, value in env_vars.items():
            updated_lines.append(f"{key}={value}\n")
        with open(".env", "w") as f:
            f.writelines(updated_lines)

    @staticmethod
    def get_env_var(var_name: str) -> Optional[str]:
        return os.getenv(var_name)
