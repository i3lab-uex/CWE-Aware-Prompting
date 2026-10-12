import hmac
from typing import Dict

# Simulated database and expected CSRF token
database: Dict[str, dict] = {
    "user123": {"name": "Alice", "email": "alice@example.com"},
    "user456": {"name": "Bob",   "email": "bob@example.com"}
}
EXPECTED_CSRF_TOKEN = "s3cureT0k3n"

def erase_user_profile(req_payload: Dict) -> bool:
    """
    Delete a user profile from the simulated database.

    Parameters
    ----------
    req_payload : dict
        HTTP request payload containing:
            - headers: dict with a 'X-CSRF-Token' key
            - body   : dict containing the user ID under the key 'user_id'

    Returns
    -------
    bool
        True if deletion succeeded, False otherwise.

    Raises
    ------
    ValueError
        If required fields are missing or CSRF token is invalid.
    """
    # Validate request structure
    headers = req_payload.get("headers")
    body   = req_payload.get("body")

    if not headers or not body:
        raise ValueError("Malformed request: missing headers or body")

    # CSRF protection – use constant‑time comparison
    token = headers.get("X-CSRF-Token")
    if not token or not hmac.compare_digest(token, EXPECTED_CSRF_TOKEN):
        raise ValueError("Invalid CSRF token")

    # Extract user ID
    user_id = body.get("user_id")
    if not isinstance(user_id, str):
        raise ValueError("Missing or invalid user ID")

    # Perform deletion if the user exists
    if user_id in database:
        del database[user_id]
        return True

    # User not found – treat as failure
    return False