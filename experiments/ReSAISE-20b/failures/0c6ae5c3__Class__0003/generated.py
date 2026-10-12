import hmac
from typing import Dict

# Constants and in‑memory "database" for demonstration purposes.
EXPECTED_CSRF_TOKEN = "my_secure_csrf_token"
database: Dict[str, dict] = {
    # Example user entries; keys are user IDs.
    "user123": {"name": "Alice"},
    "user456": {"name": "Bob"},
}


def erase_user_account(request_info: Dict) -> bool:
    """
    Delete a user account identified by the ID in request_info['body'].

    The function performs a CSRF token check using constant‑time comparison to
    mitigate timing attacks.  It validates the presence and type of all expected
    fields before proceeding.  If the user does not exist or any validation fails,
    the function returns False without raising an exception.

    Parameters
    ----------
    request_info : dict
        Expected keys:
            - 'headers': a mapping containing the CSRF token under 'X-CSRF-Token'.
            - 'body'   : a mapping containing the user ID under 'user_id'.

    Returns
    -------
    bool
        True if the account was removed; False otherwise.
    """
    # Basic structural validation
    if not isinstance(request_info, dict):
        return False

    headers = request_info.get("headers")
    body = request_info.get("body")

    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # Retrieve the CSRF token from headers and compare securely
    csrf_token = headers.get("X-CSRF-Token")
    if not isinstance(csrf_token, str):
        return False

    # Use constant‑time comparison to avoid timing attacks (CWE‑345)
    if not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # Retrieve user ID from the request body
    user_id = body.get("user_id")
    if not isinstance(user_id, str):
        return False

    # Attempt to delete the user from the database
    if user_id in database:
        try:
            del database[user_id]
            return True
        except Exception:
            # Any unexpected error during deletion should not expose details
            return False

    # User does not exist; silently fail (no information leak)
    return False