import json
from typing import Dict, Any

# Constants and mock database (would normally be in a separate module)
EXPECTED_CSRF_TOKEN = "expected_csrf_token_12345"
database: Dict[int, Any] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    # ... other user records
}

def remove_user_account(req: Dict[str, Any]) -> bool:
    """
    Remove a user account identified by `user_id` from the mock database.

    Parameters
    ----------
    req : dict
        Representation of an HTTP request. Expected to contain:
          - 'headers': a dict with at least the key 'X-CSRF-Token'
          - 'body'   : a JSON string or dict containing the key 'user_id'

    Returns
    -------
    bool
        True if a user record was found and deleted, False otherwise.
    """
    # 1. CSRF protection: verify the token is present and matches the expected value
    headers = req.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        # Token missing or incorrect -> possible CSRF attack
        return False

    # 2. Extract the user ID from the request body
    raw_body = req.get("body")
    if raw_body is None:
        return False

    # The body may already be a dict or may be a JSON string
    try:
        if isinstance(raw_body, str):
            body = json.loads(raw_body)
        else:
            body = raw_body
    except (json.JSONDecodeError, TypeError):
        return False

    user_id = body.get("user_id")
    if not isinstance(user_id, int):
        # Accept numeric strings as well
        try:
            user_id = int(user_id)
        except (TypeError, ValueError):
            return False

    # 3. Attempt to delete the user from the database
    try:
        if user_id in database:
            del database[user_id]
            return True
        else:
            # User does not exist; treat as failure to remove
            return False
    except Exception:
        # Any unexpected error (e.g., concurrent modification) is treated as failure
        return False

# Example usage (for testing purposes only):
if __name__ == "__main__":
    # Successful deletion
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": json.dumps({"user_id": 1})
    }
    print(remove_user_account(request))  # True

    # CSRF token missing
    request_bad_token = {
        "headers": {"X-CSRF-Token": "bad"},
        "body": json.dumps({"user_id": 2})
    }
    print(remove_user_account(request_bad_token))  # False

    # Non-existent user
    request_nonexistent = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": json.dumps({"user_id": 999})
    }
    print(remove_user_account(request_nonexistent))  # False