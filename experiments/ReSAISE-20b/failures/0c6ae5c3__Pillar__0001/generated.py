import hmac
from typing import Dict

# Contextual constants (would normally be defined elsewhere)
EXPECTED_CSRF_TOKEN = "s3cureT0k3n"  # Example token

def erase_user_account(
    request_info: Dict[str, any],
    database: Dict[int, dict]
) -> bool:
    """
    Deletes a user account from the in-memory `database` if the request
    contains a valid CSRF token and a known user ID.

    Parameters
    ----------
    request_info : dict
        Dictionary representing an HTTP request. Expected keys:
            - 'headers': dict, must contain 'X-CSRF-Token'
            - 'body'   : dict, must contain 'user_id' (int)
    database : dict
        In-memory dictionary mapping user IDs to user data.

    Returns
    -------
    bool
        True if the account was successfully deleted, False otherwise.
    """
    # 1. Validate presence of required keys
    headers = request_info.get("headers", {})
    body = request_info.get("body", {})

    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # 2. Retrieve and validate CSRF token using constant‑time comparison
    csrf_token = headers.get("X-CSRF-Token")
    if not isinstance(csrf_token, str):
        return False

    # Constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # 3. Retrieve and validate user ID
    user_id = body.get("user_id")
    if not isinstance(user_id, int):
        return False

    # 4. Check existence and delete the user
    if user_id in database:
        del database[user_id]
        return True

    # User ID not found
    return False