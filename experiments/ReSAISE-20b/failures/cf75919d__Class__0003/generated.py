import hmac
from typing import Dict, Any

# Simulated database: keys are user IDs (int), values are user data dicts
database: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
}

# Expected CSRF token for validation
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_123"


def delete_user_account(request: Dict[str, Any]) -> bool:
    """
    Deletes a user account from the simulated database.

    Parameters
    ----------
    request : dict
        The HTTP request representation containing:
            - headers: dict, should include 'X-CSRF-Token'
            - body   : dict, should contain 'user_id'

    Returns
    -------
    bool
        True if the user was successfully deleted, False otherwise.
    """
    # 1. Validate CSRF token
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not isinstance(csrf_token, str):
        return False
    # Constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # 2. Extract and validate user ID
    body = request.get("body", {})
    user_id_raw = body.get("user_id")
    try:
        user_id = int(user_id_raw)
    except (TypeError, ValueError):
        return False

    # 3. Check existence and delete
    if user_id not in database:
        return False

    # Perform deletion
    del database[user_id]
    return True


# Example usage (for demonstration only; remove or comment out in production)
if __name__ == "__main__":
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1}
    }
    result = delete_user_account(req)
    print("Deleted:", result)          # Should print: Deleted: True
    print("Remaining DB:", database)   # Should not contain user 1