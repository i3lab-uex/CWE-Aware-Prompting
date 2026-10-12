import hmac
from typing import Dict

# Simulated data store and CSRF token
database: Dict[str, dict] = {}
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_123"

def erase_user_profile(req_payload: Dict) -> bool:
    """
    Remove a user account from the simulated database.

    Parameters
    ----------
    req_payload : dict
        HTTP request payload containing headers and body.
        Expected structure:
            {
                "headers": {"X-CSRF-Token": "<token>"},
                "body":   {"user_id": "<id>"}
            }

    Returns
    -------
    bool
        True if the user was found and deleted, False otherwise.
    """
    # Validate request structure
    try:
        headers = req_payload["headers"]
        body = req_payload["body"]
        user_id = str(body["user_id"])
    except (KeyError, TypeError):
        return False

    # Verify CSRF token using constant‑time comparison
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # Delete user if present
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False