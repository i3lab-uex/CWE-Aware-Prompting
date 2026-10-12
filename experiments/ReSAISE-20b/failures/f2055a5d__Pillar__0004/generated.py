import re
from typing import Dict

# Expected CSRF token (should be securely stored in production)
EXPECTED_CSRF_TOKEN: str = "secure_expected_token"

def remove_user_account(input_request: Dict[str, object], database: Dict[int, dict]) -> bool:
    """
    Delete a user account from the in-memory database after validating CSRF token and input.

    Parameters
    ----------
    input_request : dict
        Dictionary representing an HTTP request. Expected keys:
            - 'headers': dict containing 'X-CSRF-Token'
            - 'body':   dict containing 'user_id' (int)
    database : dict
        In-memory dictionary simulating the user database. Keys are integer user IDs.

    Returns
    -------
    bool
        True if the account was successfully deleted, False otherwise.
    """
    # Validate presence of headers and body
    if not isinstance(input_request, dict):
        return False

    headers = input_request.get("headers", {})
    body = input_request.get("body", {})

    # 1. CSRF protection: ensure token matches expected value
    csrf_token = headers.get("X-CSRF-Token")
    if not isinstance(csrf_token, str) or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Validate user_id: must be an integer and positive
    user_id = body.get("user_id")
    if not isinstance(user_id, int) or user_id <= 0:
        return False

    # 3. Check if the user exists in the database
    if user_id not in database:
        return False

    # 4. Delete the user entry
    try:
        del database[user_id]
    except Exception:
        # In a real system we would log this error
        return False

    return True