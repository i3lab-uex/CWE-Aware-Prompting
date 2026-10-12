import hmac
import secrets

# Simulated global data store and CSRF token
database = {
    1: {"name": "Alice"},
    2: {"name": "Bob"},
    3: {"name": "Charlie"}
}
EXPECTED_CSRF_TOKEN = secrets.token_hex(16)  # Example token


def _secure_compare(a: str, b: str) -> bool:
    """
    Perform a constant‑time comparison to mitigate timing attacks.
    """
    return hmac.compare_digest(a.encode(), b.encode())


def remove_account(request: dict) -> bool:
    """
    Remove a user account from the system.

    Parameters
    ----------
    request : dict
        An HTTP request representation containing headers and a JSON body.
        Expected structure:
            {
                "headers": {"X-CSRF-Token": "<token>"},
                "body":   {"user_id": 123}
            }

    Returns
    -------
    bool
        True if the account was successfully deleted, False otherwise.
    """
    # 1. Validate CSRF token
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or not _secure_compare(csrf_token, EXPECTED_CSRF_TOKEN):
        # Invalid or missing token
        return False

    # 2. Extract and validate user ID from body
    body = request.get("body", {})
    raw_user_id = body.get("user_id")
    if raw_user_id is None:
        return False

    try:
        user_id = int(raw_user_id)
    except (ValueError, TypeError):
        # Non‑numeric user ID
        return False

    # 3. Perform deletion atomically (simulate atomicity)
    if user_id in database:
        del database[user_id]
        return True

    # User does not exist
    return False