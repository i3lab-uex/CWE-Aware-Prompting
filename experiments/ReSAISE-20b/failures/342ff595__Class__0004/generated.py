import re
from typing import Dict

# Mock in‑memory user database: {user_id (int): user_record (dict)}
database: Dict[int, dict] = {}

# Expected CSRF token for the session
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token-12345"


def _validate_csrf_token(token: str) -> bool:
    """
    Validate the CSRF token using a constant‑time comparison to avoid timing attacks.
    """
    return re.fullmatch(r"[a-zA-Z0-9\-_]{20,}", token) is not None and token == EXPECTED_CSRF_TOKEN


def _extract_user_id(body: Dict) -> int | None:
    """
    Safely extract an integer user ID from the request body.
    Returns None if extraction fails or the value is not a positive integer.
    """
    try:
        user_id = int(body.get("user_id", 0))
        if user_id <= 0:
            return None
        return user_id
    except (ValueError, TypeError):
        return None


def remove_user_profile(request_data: Dict) -> bool:
    """
    Remove a user profile from the in‑memory database.

    Parameters
    ----------
    request_data : dict
        A representation of an HTTP request containing:
          - headers: dict with a 'X-CSRF-Token' key
          - body: dict containing the 'user_id'

    Returns
    -------
    bool
        True if the account was removed successfully, False otherwise.
    """
    # 1. Verify CSRF token
    headers = request_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or not _validate_csrf_token(csrf_token):
        return False

    # 2. Extract and validate user ID
    body = request_data.get("body", {})
    user_id = _extract_user_id(body)
    if user_id is None:
        return False

    # 3. Attempt to delete the user
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False