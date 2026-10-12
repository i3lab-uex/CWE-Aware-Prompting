import re
from typing import Dict, Any

# Mock in‑memory user database: {user_id: user_record}
database: Dict[int, Any] = {}

# Expected CSRF token (normally stored securely)
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_value"

def remove_user_data(data: Dict[str, Any]) -> bool:
    """
    Remove a user account from the in‑memory database.

    Parameters
    ----------
    data : dict
        Dictionary representing an HTTP request. Expected keys:
            - 'headers': mapping of header names to values
            - 'body'   : mapping that contains the user ID and CSRF token

    Returns
    -------
    bool
        True if deletion succeeded, False otherwise.

    Notes
    -----
    - Validates the CSRF token to mitigate cross‑site request forgery.
    - Sanitises the user ID input, ensuring it is a positive integer.
    - Removes the record only if it exists in the database.
    """
    # 1. Extract headers and body safely
    try:
        headers = data.get("headers", {})
        body   = data.get("body", {})
    except AttributeError:
        # Data is not a dict or missing expected structure
        return False

    # 2. CSRF token validation (case‑sensitive)
    csrf_token = body.get("csrf_token")
    if not isinstance(csrf_token, str) or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 3. Extract and sanitise user ID
    raw_user_id = body.get("user_id")
    if raw_user_id is None:
        return False

    # Allow numeric string or int, reject other types
    if isinstance(raw_user_id, int):
        user_id = raw_user_id
    elif isinstance(raw_user_id, str) and re.fullmatch(r"\d+", raw_user_id):
        user_id = int(raw_user_id)
    else:
        return False

    # Ensure the ID is positive
    if user_id <= 0:
        return False

    # 4. Delete the user record if it exists
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False