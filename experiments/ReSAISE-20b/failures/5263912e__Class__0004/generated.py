import json
from typing import Dict, Any

# Constants and mock database for demonstration purposes
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token-123"
database: Dict[int, Any] = {
    1: {"name": "Alice"},
    2: {"name": "Bob"},
    3: {"name": "Charlie"}
}


def remove_user_account(req: Dict[str, Any]) -> bool:
    """
    Remove a user account from the mock database.

    Parameters
    ----------
    req : dict
        A representation of an HTTP request containing:
          - 'headers': a mapping that may contain the CSRF token under
            the key 'X-CSRF-Token'.
          - 'body': a JSON string or dict containing a field
            'user_id' (int).

    Returns
    -------
    bool
        True if the account was removed successfully, False otherwise.
    """
    # 1. Verify CSRF token
    headers = req.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF verification failed
        return False

    # 2. Extract user_id from the body
    body = req.get("body")
    if isinstance(body, str):
        try:
            body_data = json.loads(body)
        except json.JSONDecodeError:
            return False
    elif isinstance(body, dict):
        body_data = body
    else:
        # Unsupported body type
        return False

    user_id = body_data.get("user_id")
    if not isinstance(user_id, int):
        # Invalid or missing user_id
        return False

    # 3. Attempt to delete the user from the database
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False