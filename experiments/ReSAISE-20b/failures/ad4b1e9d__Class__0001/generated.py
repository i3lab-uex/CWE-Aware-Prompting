import hmac
from typing import Dict

# Simulated database and CSRF token
database: Dict[int, dict] = {}
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token"

def erase_user_profile(req_payload: Dict) -> bool:
    """
    Remove a user account from the simulated database.

    Parameters
    ----------
    req_payload : dict
        Dictionary representing an HTTP request. Expected to contain:
            - 'headers': mapping of header names to values
            - 'body': mapping that includes the key 'user_id'

    Returns
    -------
    bool
        True if the user was successfully deleted, False otherwise.
    """
    # 1. Validate CSRF token
    headers = req_payload.get("headers", {})
    incoming_token = headers.get("X-CSRF-Token")
    if not incoming_token:
        return False
    # Constant-time comparison to mitigate timing attacks
    if not hmac.compare_digest(incoming_token, EXPECTED_CSRF_TOKEN):
        return False

    # 2. Extract and validate user_id
    body = req_payload.get("body", {})
    user_id_raw = body.get("user_id")
    if user_id_raw is None:
        return False
    try:
        # Accept only integers; reject strings that look like ints to avoid type confusion
        if isinstance(user_id_raw, int):
            user_id = user_id_raw
        elif isinstance(user_id_raw, str) and user_id_raw.isdigit():
            user_id = int(user_id_raw)
        else:
            return False
    except (ValueError, TypeError):
        return False

    # 3. Delete the user if present
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False