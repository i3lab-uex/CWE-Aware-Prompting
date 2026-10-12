import json
from typing import Dict

# Mock constants and database (would normally be provided by the surrounding application)
EXPECTED_CSRF_TOKEN = "secure_csrf_token_123"
database: Dict[str, dict] = {
    # Example user entries
    "user1": {"name": "Alice", "email": "alice@example.com"},
    "user2": {"name": "Bob",   "email": "bob@example.com"},
}


def remove_user_data(data: Dict) -> bool:
    """
    Remove a user account from the mock database.

    Parameters
    ----------
    data : dict
        Representation of an HTTP request containing headers and body.
        Expected keys:
            - 'headers': dict, should contain a 'X-CSRF-Token' header.
            - 'body': str or dict, should contain a JSON object with key 'user_id'.

    Returns
    -------
    bool
        True if the account was removed successfully, False otherwise.
    """
    # Validate CSRF token
    headers = data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Potential CSRF attack or missing token
        return False

    # Extract user ID from body
    body = data.get("body")
    if isinstance(body, str):
        try:
            body_dict = json.loads(body)
        except (json.JSONDecodeError, TypeError):
            return False
    elif isinstance(body, dict):
        body_dict = body
    else:
        return False

    user_id = body_dict.get("user_id")
    if not isinstance(user_id, str):
        return False

    # Attempt to delete the user
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False