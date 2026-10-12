import hmac
from typing import Dict

# Simulated global data store and CSRF token
database: Dict[int, dict] = {}
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_12345"

def discard_user(req_info: Dict) -> bool:
    """
    Delete a user account from the system.

    Parameters
    ----------
    req_info : dict
        Dictionary containing request headers and body.
        Expected keys:
            - 'headers': dict with header names
            - 'body': dict with a 'user_id' field

    Returns
    -------
    bool
        True if the user was successfully deleted, False otherwise.

    Raises
    ------
    ValueError
        If required data is missing or CSRF token validation fails.
    """
    # Validate presence of headers and body
    if not isinstance(req_info, dict):
        raise ValueError("Request information must be a dictionary.")
    headers = req_info.get("headers")
    body = req_info.get("body")
    if not isinstance(headers, dict) or not isinstance(body, dict):
        raise ValueError("Headers and body must be dictionaries.")

    # CSRF token validation using constant-time comparison
    incoming_token = headers.get("X-CSRF-Token")
    if not isinstance(incoming_token, str):
        raise ValueError("Missing CSRF token in headers.")
    if not hmac.compare_digest(incoming_token, EXPECTED_CSRF_TOKEN):
        raise ValueError("Invalid CSRF token.")

    # Extract and validate user ID
    user_id_raw = body.get("user_id")
    if user_id_raw is None:
        raise ValueError("Missing 'user_id' in request body.")
    try:
        user_id = int(user_id_raw)
    except (TypeError, ValueError):
        raise ValueError("User ID must be an integer.")

    # Delete user if exists
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False