import re
from typing import Dict

# Constants and mock database (for illustration purposes)
EXPECTED_CSRF_TOKEN = "secure_csrf_token_12345"
database: Dict[str, dict] = {
    # Example user entries
    "user1": {"name": "Alice", "email": "alice@example.com"},
    "user2": {"name": "Bob",   "email": "bob@example.com"},
}

def remove_user_profile(request_data: Dict) -> bool:
    """
    Remove a user profile from the in-memory `database`.

    Parameters
    ----------
    request_data : dict
        A representation of an HTTP request containing:
            - headers: dict with 'X-CSRF-Token' header
            - body   : dict containing 'user_id'

    Returns
    -------
    bool
        True if the user was removed successfully, False otherwise.

    Raises
    ------
    ValueError
        If required fields are missing or malformed.
    """
    # Validate request structure
    if not isinstance(request_data, dict):
        raise ValueError("request_data must be a dictionary")

    headers = request_data.get("headers")
    body   = request_data.get("body")

    if not isinstance(headers, dict) or not isinstance(body, dict):
        raise ValueError("headers and body must be dictionaries")

    # 1. CSRF protection: compare tokens in constant time
    csrf_token = headers.get("X-CSRF-Token")
    if not isinstance(csrf_token, str):
        return False

    # Constant-time comparison to mitigate timing attacks
    def constant_time_compare(a: str, b: str) -> bool:
        if len(a) != len(b):
            return False
        result = 0
        for x, y in zip(a.encode(), b.encode()):
            result |= x ^ y
        return result == 0

    if not constant_time_compare(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # 2. Validate user_id format (e.g., alphanumeric, 3-20 chars)
    user_id = body.get("user_id")
    if not isinstance(user_id, str):
        return False

    if not re.fullmatch(r"[a-zA-Z0-9_]{3,20}", user_id):
        return False

    # 3. Remove the user if present
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False