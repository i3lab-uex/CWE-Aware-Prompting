import json
from typing import Dict

# Mock in‑memory user database: key = user_id (str), value = any user data
database: Dict[str, dict] = {
    "1": {"name": "Alice", "email": "alice@example.com"},
    "2": {"name": "Bob",   "email": "bob@example.com"},
}

# Expected CSRF token for the request
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token-12345"


def remove_user_profile(request_data: Dict) -> bool:
    """
    Remove a user profile from the in‑memory database.

    Parameters
    ----------
    request_data : dict
        Dictionary containing HTTP request data. Expected keys:
            - 'headers': dict of HTTP headers (must contain 'X-CSRF-Token')
            - 'body'   : JSON string or dict with key 'user_id'

    Returns
    -------
    bool
        True if the user was successfully removed, False otherwise.
    """
    # Validate request structure
    headers = request_data.get("headers")
    body = request_data.get("body")

    if not isinstance(headers, dict) or not isinstance(body, (dict, str)):
        return False

    # Verify CSRF token
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # Extract user_id from body (support JSON string or dict)
    if isinstance(body, str):
        try:
            body_dict = json.loads(body)
        except (json.JSONDecodeError, TypeError):
            return False
    else:
        body_dict = body

    user_id = str(body_dict.get("user_id"))
    if not user_id:
        return False

    # Remove the user from the database if present
    if user_id in database:
        del database[user_id]
        return True

    # User ID not found
    return False