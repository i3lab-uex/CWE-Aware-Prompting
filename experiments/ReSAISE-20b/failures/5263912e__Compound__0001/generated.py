# remove_user_account.py

from typing import Dict, Any

# Mock database: user_id -> user_record
database: Dict[str, Any] = {
    "user123": {"name": "Alice", "email": "alice@example.com"},
    "user456": {"name": "Bob",   "email": "bob@example.com"},
}

# Expected CSRF token for this example
EXPECTED_CSRF_TOKEN = "s3cUrE-t0kEn-12345"

def remove_user_account(req: Dict[str, Any]) -> bool:
    """
    Remove a user account identified by `user_id` from the mock database.

    Parameters
    ----------
    req : dict
        A representation of an HTTP request containing:
            - headers: a dict with 'X-CSRF-Token' key.
            - body: a dict containing the 'user_id'.

    Returns
    -------
    bool
        True if deletion succeeded, False otherwise.

    Security
    --------
    - CSRF protection: verifies the token matches EXPECTED_CSRF_TOKEN.
    - Input validation: ensures user_id is a string and exists in the database.
    """
    # 1. CSRF token validation
    headers = req.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Token missing or incorrect -> reject
        return False

    # 2. Retrieve and validate user_id from request body
    body = req.get("body", {})
    user_id = body.get("user_id")
    if not isinstance(user_id, str) or not user_id:
        return False

    # 3. Attempt to delete the user from the database
    if user_id in database:
        # Use pop with default to avoid KeyError
        database.pop(user_id, None)
        return True

    # User not found
    return False