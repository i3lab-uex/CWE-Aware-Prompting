import hmac
from typing import Dict

# Simulated global data store and CSRF token (would normally be in a secure config)
database: Dict[str, dict] = {
    "user1": {"name": "Alice"},
    "user2": {"name": "Bob"},
}
EXPECTED_CSRF_TOKEN = "s3cr3t_csrf_token"

def _constant_time_compare(val1: str, val2: str) -> bool:
    """
    Compare two strings in constant time to mitigate timing attacks.
    """
    return hmac.compare_digest(val1, val2)

def remove_account(request: Dict) -> bool:
    """
    Remove a user account from the database after validating CSRF token.

    Parameters
    ----------
    request : dict
        HTTP request representation containing:
            - headers: dict, should include 'X-CSRF-Token'
            - body: dict, should include 'user_id'

    Returns
    -------
    bool
        True if deletion succeeded, False otherwise.

    Notes
    -----
    - Raises no exceptions; failures are signaled via the return value.
    - Uses constant-time comparison for CSRF token to avoid timing attacks.
    """
    # Validate presence of headers and body
    headers = request.get("headers", {})
    body = request.get("body", {})

    # CSRF token validation
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or not _constant_time_compare(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # Extract user ID
    user_id = body.get("user_id")
    if not isinstance(user_id, str):
        return False

    # Delete user from database if exists
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False