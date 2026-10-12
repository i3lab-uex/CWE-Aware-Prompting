import json
from typing import Dict, Any

# Simulated database and CSRF token
database: Dict[int, Dict[str, Any]] = {}
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_12345"

def delete_user_account(request: Dict[str, Any]) -> bool:
    """
    Deletes a user account from the simulated database.

    Parameters
    ----------
    request : dict
        Dictionary containing HTTP headers and body. Expected keys:
            - 'headers': dict with a 'X-CSRF-Token' header.
            - 'body': JSON string or dict containing the user ID under key 'user_id'.

    Returns
    -------
    bool
        True if deletion succeeded, False otherwise.

    Raises
    ------
    ValueError
        If required fields are missing or malformed.
    """
    # 1. Validate CSRF token
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token:
        return False
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract user ID from body
    body = request.get("body")
    if body is None:
        return False

    # Body may be a dict or JSON string
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            return False

    user_id_raw = body.get("user_id")
    if user_id_raw is None:
        return False

    # Ensure the ID is an integer (or convertible)
    try:
        user_id = int(user_id_raw)
    except (TypeError, ValueError):
        return False

    # 3. Delete user if exists
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False