import hmac
import hashlib

# Simulated database and CSRF token for the example
database = {
    1: {"name": "Alice"},
    2: {"name": "Bob"},
    3: {"name": "Charlie"}
}
EXPECTED_CSRF_TOKEN = "secure_csrf_token_12345"

def remove_account(request: dict) -> bool:
    """
    Remove a user account from the simulated database.

    Parameters
    ----------
    request : dict
        HTTP request representation. Expected keys:
            - 'headers': dict containing at least 'X-CSRF-Token'
            - 'body'   : dict containing 'user_id'

    Returns
    -------
    bool
        True if the account was deleted, False otherwise.
    """
    # 1. Verify CSRF token using constant‑time comparison
    headers = request.get("headers", {})
    incoming_token = headers.get("X-CSRF-Token")
    if not incoming_token or not hmac.compare_digest(
        incoming_token.encode("utf-8"),
        EXPECTED_CSRF_TOKEN.encode("utf-8")
    ):
        # Token missing or invalid
        return False

    # 2. Validate and extract user_id from body
    body = request.get("body", {})
    try:
        # Accept only integer IDs; reject strings or other types
        user_id = int(body.get("user_id"))
    except (TypeError, ValueError):
        return False

    # 3. Check that the user exists in the database
    if user_id not in database:
        return False

    # 4. Delete the user
    try:
        del database[user_id]
        return True
    except Exception:
        # Catch unexpected deletion errors (unlikely in this simple dict)
        return False