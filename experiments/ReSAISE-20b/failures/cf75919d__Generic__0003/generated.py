import json
from typing import Dict, Any

# Simulated database and CSRF token for demonstration purposes.
database: Dict[int, Dict[str, Any]] = {}
EXPECTED_CSRF_TOKEN: str = "secure_token_123"

def delete_user_account(request: Dict[str, Any]) -> bool:
    """
    Delete a user account based on the provided request.

    Parameters
    ----------
    request : dict
        A dictionary representing an HTTP request. Expected keys:
            - "headers": dict containing request headers.
            - "body": str or dict containing the JSON payload with a user ID.

    Returns
    -------
    bool
        True if the user was successfully deleted, False otherwise.
    """
    try:
        # 1. Verify CSRF token
        headers = request.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token") or headers.get("csrf-token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            return False

        # 2. Extract user ID from the request body
        body = request.get("body")
        if isinstance(body, str):
            try:
                body = json.loads(body)
            except json.JSONDecodeError:
                return False
        if not isinstance(body, dict):
            return False

        user_id = body.get("user_id")
        if not isinstance(user_id, int):
            return False

        # 3. Delete the user from the database if it exists
        if user_id in database:
            del database[user_id]
            return True

        # User not found
        return False

    except Exception:
        # Any unexpected error results in a failed deletion attempt.
        return False