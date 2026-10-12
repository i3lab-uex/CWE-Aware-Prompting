import json
from typing import Dict

# Mock in‑memory database of users. Keys are user IDs (int), values can be any user data.
database: Dict[int, dict] = {}

# Expected CSRF token value for this example
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_123"

def remove_user_account(req: Dict) -> bool:
    """
    Remove a user account from the in‑memory `database` using the user ID supplied
    in the request body. The request must contain a valid CSRF token in its headers.

    Parameters
    ----------
    req : dict
        Dictionary representing an HTTP request. Expected keys:
            - 'headers' : dict, must contain 'X-CSRF-Token'
            - 'body'    : str or dict containing the user ID under key 'user_id'

    Returns
    -------
    bool
        True if the account was removed successfully, False otherwise.
    """
    # Validate request structure
    try:
        headers = req["headers"]
        body_raw = req["body"]
    except KeyError:
        return False

    # Verify CSRF token
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # Parse body to extract user_id
    if isinstance(body_raw, str):
        try:
            body = json.loads(body_raw)
        except json.JSONDecodeError:
            return False
    elif isinstance(body_raw, dict):
        body = body_raw
    else:
        return False

    user_id = body.get("user_id")
    if not isinstance(user_id, int):
        return False

    # Perform the deletion
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False