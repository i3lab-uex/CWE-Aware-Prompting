import hmac
from typing import Dict

# Mock in‑memory database: mapping user_id (str) -> user data dict
database: Dict[str, Dict] = {}

# Expected CSRF token for this example
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_12345"


def remove_user_profile(request_data: Dict) -> bool:
    """
    Remove a user profile from the mock database.

    Parameters
    ----------
    request_data : dict
        Dictionary representing an HTTP request. Expected keys:
            - 'headers': mapping of header names to values.
            - 'body'   : mapping that contains the key 'user_id'.

    Returns
    -------
    bool
        True if deletion succeeded, False otherwise.
    """
    # Basic validation of request structure
    headers = request_data.get("headers", {})
    body = request_data.get("body", {})

    # 1. CSRF protection: compare tokens in constant time
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # 2. Retrieve and validate user_id
    user_id = body.get("user_id")
    if not isinstance(user_id, str) or not user_id:
        return False

    # 3. Attempt deletion
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False