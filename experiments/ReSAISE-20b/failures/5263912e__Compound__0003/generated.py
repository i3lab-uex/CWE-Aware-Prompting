import re
from typing import Dict, Any

# Mock database: user_id -> user data
database: Dict[str, Dict[str, Any]] = {
    "1": {"name": "Alice", "email": "alice@example.com"},
    "2": {"name": "Bob",   "email": "bob@example.com"},
}

# Expected CSRF token
EXPECTED_CSRF_TOKEN: str = "s3cureT0k3n"

def _extract_user_id(body: Dict[str, Any]) -> str | None:
    """
    Extract the user ID from the request body.
    The ID is expected to be a string of digits; any other format
    will cause the function to return None.
    """
    user_id = body.get("user_id")
    if isinstance(user_id, str) and re.fullmatch(r"\d+", user_id):
        return user_id
    return None

def remove_user_account(req: Dict[str, Any]) -> bool:
    """
    Remove a user account from the in-memory database.

    Parameters
    ----------
    req : dict
        A representation of an HTTP request. It must contain:
          * headers: a mapping of header names to values
          * body: a mapping that includes the key 'user_id'

    Returns
    -------
    bool
        True if the account was removed successfully, otherwise False.
    """
    # 1. CSRF protection: verify the token is present and matches
    headers = req.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token") or headers.get("x-csrf-token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF token missing or incorrect
        return False

    # 2. Extract user ID safely from body
    body = req.get("body", {})
    user_id = _extract_user_id(body)
    if not user_id:
        # Invalid or missing user ID
        return False

    # 3. Delete the record if it exists
    if user_id in database:
        del database[user_id]
        return True

    # 4. User not found
    return False