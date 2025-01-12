"""
Authentication routes for Pinterest OAuth
"""

from flask import Blueprint, redirect, request, session
from services.pinterest_oauth import pinterest_oauth

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/token")
def pinterest_auth():
    """Redirect to Pinterest OAuth page"""
    auth_url = pinterest_oauth.get_auth_url()
    return redirect(auth_url)


@auth_bp.route("/callback")
def pinterest_callback():
    """Handle Pinterest OAuth callback"""
    code = request.args.get("code")
    if not code:
        return "Error: No authorization code provided", 400

    tokens = pinterest_oauth.exchange_code_for_token(code)
    if tokens:
        session["access_token"] = tokens["access_token"]
        return redirect("/")
    return "Error: Failed to get access token", 400


@auth_bp.route("/refresh")
def refresh_token():
    """Refresh the access token"""
    new_token = pinterest_oauth.refresh_access_token()
    if new_token:
        return {"access_token": new_token}
    return "Error: Failed to refresh token", 400
