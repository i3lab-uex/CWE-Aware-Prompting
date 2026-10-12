import json
from typing import Dict

# Constants and mock database (normally these would be defined elsewhere)
EXPECTED_CSRF_TOKEN = "expected_csrf_token_value"
database: Dict[str, dict] = {  # key: user_id
    "user123": {"name": "Alice", "email": "alice@example.com"},
    "user456": {"name": "Bob",   "email": "bob@example.com"},
}


def remove_user_data(data: Dict) -> bool:
    """
    Remove a user account identified by `user_id` from the in-memory `database`.

    Parameters
    ----------
    data : dict
        A representation of an HTTP request containing:
            - headers: a mapping that should include the CSRF token.
            - body: a JSON string or dict containing the `user_id` key.

    Returns
    -------
    bool
        True if the account was successfully removed, False otherwise.
    """
    # Validate CSRF token
    headers = data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Token missing or incorrect – reject the request
        return False

    # Extract user_id from body (handle both dict and JSON string)
    raw_body = data.get("body")
    if raw_body is None:
        return False

    if isinstance(raw_body, str):
        try:
            body = json.loads(raw_body)
        except json.JSONDecodeError:
            return False
    elif isinstance(raw_body, dict):
        body = raw_body
    else:
        return False

    user_id = body.get("user_id")
    if not isinstance(user_id, str):
        return False

    # Remove the user from the database if it exists
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False