import json
from typing import Dict

# Simulated in‑memory database and CSRF token
database: Dict[int, dict] = {}
EXPECTED_CSRF_TOKEN = "s3cureT0k3n"

def erase_user_account(request_info: Dict) -> bool:
    """
    Delete a user account from the in‑memory database.

    Parameters
    ----------
    request_info : dict
        Dictionary representing an HTTP request. Expected keys:
            - 'headers': dict containing the CSRF token under key 'X-CSRF-Token'
            - 'body'   : dict containing the user ID under key 'user_id'

    Returns
    -------
    bool
        True if the account was successfully deleted, False otherwise.
    """
    try:
        # Validate CSRF token
        headers = request_info.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            return False

        # Extract user ID
        body = request_info.get("body", {})
        if not isinstance(body, dict):
            return False

        user_id = body.get("user_id")
        if user_id is None:
            return False

        # Ensure user_id is an integer
        try:
            user_id = int(user_id)
        except (TypeError, ValueError):
            return False

        # Delete user if exists
        if user_id in database:
            del database[user_id]
            return True

        # User not found
        return False

    except Exception:
        # Log the exception in a real application; here we simply fail silently
        return False