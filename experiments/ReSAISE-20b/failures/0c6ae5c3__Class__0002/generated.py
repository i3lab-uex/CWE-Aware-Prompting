import hmac
from typing import Dict, Any

# Predefined CSRF token for the application (example value)
EXPECTED_CSRF_TOKEN = "super_secret_csrf_token"

def erase_user_account(request_info: Dict[str, Any], database: Dict[int, dict]) -> bool:
    """
    Delete a user account from the in-memory database.

    Parameters
    ----------
    request_info : dict
        HTTP request representation. Expected keys:
            - 'headers': dict containing a 'X-CSRF-Token' entry.
            - 'body': dict containing a 'user_id' entry (int or str convertible to int).
    database : dict
        In-memory user database mapping user IDs (int) to user data.

    Returns
    -------
    bool
        True if the account was deleted successfully, False otherwise.
    """
    # 1. Verify request structure
    headers = request_info.get("headers")
    body = request_info.get("body")
    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # 2. Verify CSRF token using constant‑time comparison
    csrf_token = headers.get("X-CSRF-Token")
    if not isinstance(csrf_token, str):
        return False
    if not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # 3. Extract and validate user ID
    user_id_raw = body.get("user_id")
    if user_id_raw is None:
        return False
    try:
        user_id = int(user_id_raw)
    except (TypeError, ValueError):
        return False

    # 4. Attempt to delete the user
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False