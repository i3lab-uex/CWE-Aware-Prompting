import hmac
import hashlib

# Simulated data store: mapping user IDs (int) to user records
database = {
    1: {"name": "Alice"},
    2: {"name": "Bob"},
    3: {"name": "Charlie"}
}

# Expected CSRF token (in a real app this would be stored per session)
EXPECTED_CSRF_TOKEN = "super_secret_csrf_token"

def remove_account(request: dict) -> bool:
    """
    Remove a user account identified by the `user_id` field in the request body.

    Parameters
    ----------
    request : dict
        HTTP request representation. Must contain:
            - 'headers': mapping of header names to values (case‑insensitive).
            - 'body'   : mapping that includes a 'user_id' key.

    Returns
    -------
    bool
        True if the account was deleted, False otherwise.
    """
    # 1. Verify CSRF token
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token") or headers.get("x-csrf-token")
    if not csrf_token:
        return False

    # Use constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # 2. Extract user_id from body
    body = request.get("body", {})
    if not isinstance(body, dict):
        return False

    user_id = body.get("user_id")
    if not isinstance(user_id, int):
        return False

    # 3. Delete user from the database if present
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False