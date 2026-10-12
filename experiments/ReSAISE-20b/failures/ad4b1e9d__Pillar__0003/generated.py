import hmac
from typing import Dict

# Simulated data store and CSRF token (would normally be configured elsewhere)
database: Dict[str, dict] = {}
EXPECTED_CSRF_TOKEN: str = "secure_expected_token"

def erase_user_profile(req_payload: Dict) -> bool:
    """
    Deletes a user account from the simulated database.

    Parameters
    ----------
    req_payload : dict
        A dictionary representing an HTTP request. It must contain:
            - 'headers': a mapping with at least the key 'X-CSRF-Token'.
            - 'body': a mapping that includes a numeric or string user identifier under the key 'user_id'.

    Returns
    -------
    bool
        True if deletion succeeded, False otherwise.
    """
    try:
        headers = req_payload["headers"]
        body = req_payload["body"]
    except (KeyError, TypeError):
        # Malformed request
        return False

    # 1. CSRF protection – use constant‑time comparison to avoid timing attacks
    incoming_token = headers.get("X-CSRF-Token", "")
    if not isinstance(incoming_token, str):
        return False
    if not hmac.compare_digest(incoming_token, EXPECTED_CSRF_TOKEN):
        return False

    # 2. Validate user_id – must be a string or integer, no other types allowed
    user_id = body.get("user_id")
    if not isinstance(user_id, (str, int)):
        return False

    # Convert integer IDs to string for consistent key usage
    user_key = str(user_id)

    # 3. Delete the user if it exists
    if user_key in database:
        del database[user_key]
        return True

    # User not found
    return False