import json
from typing import Dict, Any

# Predefined CSRF token expected by the server
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_value"

def remove_user_account(input_request: Dict[str, Any], database: Dict[int, Any]) -> bool:
    """
    Deletes a user account from the in-memory `database`.

    Parameters
    ----------
    input_request : dict
        Dictionary representing an HTTP request. It must contain:
            - 'headers': a dictionary that includes the key 'X-CSRF-Token'.
            - 'body'   : a JSON string or dictionary that contains the key 'user_id'.
    database : dict
        In-memory dictionary simulating a user database. Keys are integer user IDs.

    Returns
    -------
    bool
        True if the account was successfully deleted; False otherwise.
    """
    # 1. Verify CSRF token
    headers = input_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid or missing CSRF token
        return False

    # 2. Extract user_id from body
    raw_body = input_request.get("body")
    if raw_body is None:
        return False

    # Body may be a dict or a JSON string
    if isinstance(raw_body, str):
        try:
            body = json.loads(raw_body)
        except (json.JSONDecodeError, TypeError):
            return False
    elif isinstance(raw_body, dict):
        body = raw_body
    else:
        return False

    user_id = body.get("user_id")
    if not isinstance(user_id, int):
        # Ensure the user ID is an integer to prevent accidental deletion of keys
        return False

    # 3. Delete the user if present
    try:
        del database[user_id]
    except KeyError:
        # User ID not found
        return False

    # 4. Successfully removed
    return True