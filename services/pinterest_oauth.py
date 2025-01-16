"""
Pinterest OAuth Service
Handles authentication and token management for Pinterest API
"""

import base64
import requests
from typing import Optional, Dict, Any
from dataclasses import dataclass
from flask import session
from utils_old import get_env_var, save_tokens_to_env
from utils.env_manager import EnvManager

@dataclass
class OAuthConfig:
    """Configuration for Pinterest OAuth"""

    client_id: str
    client_secret: str
    redirect_uri: str
    auth_url: str = "https://www.pinterest.com/oauth/"
    token_url: str = "https://api.pinterest.com/v5/oauth/token"
    scope: str = "boards:read pins:write pins:read boards:write"


class PinterestOAuthService:
    """Service for handling Pinterest OAuth operations"""

    def __init__(self):
        """Initialize the OAuth service with configuration from environment variables"""
        self.config = OAuthConfig(
            client_id=EnvManager.get_env_var("PINTEREST_CLIENT_ID"),
            client_secret=EnvManager.get_env_var("PINTEREST_CLIENT_SECRET"),
            redirect_uri=EnvManager.get_env_var("PINTEREST_REDIRECT_URI"),
        )

    def get_auth_url(self) -> str:
        """Generate the Pinterest OAuth authorization URL"""
        auth_params = {
            "client_id": self.config.client_id,
            "redirect_uri": self.config.redirect_uri,
            "response_type": "code",
            "scope": self.config.scope,
            "state": "random_state_string",  # In production, use a secure random string
        }

        return (
            f"{self.config.auth_url}"
            f"?client_id={auth_params['client_id']}"
            f"&redirect_uri={auth_params['redirect_uri']}"
            f"&response_type={auth_params['response_type']}"
            f"&scope={auth_params['scope']}"
            f"&state={auth_params['state']}"
        )

    def _get_basic_auth_header(self) -> Dict[str, str]:
        """Generate the Basic Auth header for token requests"""
        token_data = f"{self.config.client_id}:{self.config.client_secret}"
        encoded_token = base64.b64encode(token_data.encode()).decode("utf-8")

        return {
            "Authorization": f"Basic {encoded_token}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

    def exchange_code_for_token(self, code: str) -> Optional[Dict[str, Any]]:
        """Exchange authorization code for access and refresh tokens"""
        try:
            data = {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": self.config.redirect_uri,
            }

            response = requests.post(
                self.config.token_url, headers=self._get_basic_auth_header(), data=data
            )

            if response.status_code == 200:
                tokens = response.json()
                EnvManager.save_tokens(tokens)
                return tokens

            return None

        except Exception as e:
            print(f"Error exchanging code for token: {e}")
            return None

    def refresh_access_token(
        self, refresh_token: Optional[str] = None
    ) -> Optional[str]:
        """Refresh the access token using a refresh token"""
        try:
            if not refresh_token:
                refresh_token = EnvManager.get_env_var("REFRESH_TOKEN")

            if not refresh_token:
                print("Error: No refresh token available.")
                return None

            data = {
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": self.config.client_id,
                "client_secret": self.config.client_secret,
            }

            response = requests.post(self.config.token_url, data=data)

            if response.status_code == 200:
                tokens = response.json()
                session["access_token"] = tokens["access_token"]
                save_tokens_to_env({"access_token": tokens["access_token"]})
                return tokens["access_token"]

            return None

        except Exception as e:
            print(f"Error refreshing token: {e}")
            return None


# Create a singleton instance
pinterest_oauth = PinterestOAuthService()
