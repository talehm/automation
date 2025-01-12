import requests
import base64
from flask import session
from .config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, AUTH_URL, TOKEN_URL
from utils import load_env_vars, save_tokens_to_env, get_env_var


def get_pinterest_auth_url():
    auth_params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "boards:read pins:write pins:read boards:write",
        "state": "random_state_string",
    }
    auth_url = f"{AUTH_URL}?client_id={auth_params['client_id']}&redirect_uri={auth_params['redirect_uri']}&response_type={auth_params['response_type']}&scope={auth_params['scope']}&state={auth_params['state']}"
    return auth_url


def exchange_code_for_token(code):
    token_data = f"{CLIENT_ID}:{CLIENT_SECRET}"
    encoded_token = base64.b64encode(token_data.encode())
    headers = {
        "Authorization": "Basic " + encoded_token.decode("utf-8"),
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }
    response = requests.post(TOKEN_URL, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()  # access_token, refresh_token, expires_in
    return None


def refresh_access_token():
    # refresh_token = session.get("refresh_token")
    refresh_token = None
    if not refresh_token:
        return "Error: No refresh token available."

    refresh_data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    response = requests.post(TOKEN_URL, data=refresh_data)
    if response.status_code == 200:
        tokens = response.json()
        session["access_token"] = tokens["access_token"]
        return tokens["access_token"]
    return None
