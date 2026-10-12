import json
from typing import Dict

# Constants and mock database (to be provided by the surrounding application)
EXPECTED_CSRF_TOKEN: str = "known_csrf_token_value"
database: Dict[str, dict] = {
    # Example entries
    "user1": {"name": "Alice"},
    "user2": {"name": "Bob"},
}

def remove_user_account(req: Dict) -> bool:
    """
    Remove a user account identified by `user_id` from the mock database.

    Parameters
    ----------
    req : dict
        Representation of an HTTP request. Expected keys:
            - 'headers': dict containing request headers (e.g., 'X-CSRF-Token')
            - 'body'   : JSON string or dict containing 'user_id'

    Returns
    -------
    bool
        True if the account was removed, False otherwise.

    Raises
    ------
    None
    """
    try:
        # 1. Validate CSRF token (header must match expected value)
        headers = req.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token") or headers.get("x-csrf-token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            # CSRF validation failed
            return False

        # 2. Extract user_id from request body
        body = req.get("body")
        if isinstance(body, str):
            try:
                body_data = json.loads(body)
            except json.JSONDecodeError:
                return False
        elif isinstance(body, dict):
            body_data = body
        else:
            return False

        user_id = body_data.get("user_id")
        if not isinstance(user_id, str):
            return False

        # 3. Remove user from database if present
        if user_id in database:
            del database[user_id]
            return True

        # User not found
        return False

    except Exception:
        # Any unexpected error should result in a safe failure
        return False