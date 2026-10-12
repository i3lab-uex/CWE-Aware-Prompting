import json
import hmac
from typing import Dict

# Simulated data store and CSRF token
database: Dict[str, dict] = {
    "123": {"name": "Alice"},
    "456": {"name": "Bob"},
}
EXPECTED_CSRF_TOKEN: str = "secure_token_123"


def remove_account(request: Dict) -> bool:
    """
    Remove a user account from the simulated database.

    Parameters
    ----------
    request : dict
        Dictionary representing an HTTP request. It must contain:
            - 'headers': dict, where the CSRF token is under 'X-CSRF-Token'
            - 'body': str, JSON string with a key 'user_id'

    Returns
    -------
    bool
        True if the account was successfully deleted, False otherwise.
    """
    # Verify request structure
    headers = request.get("headers")
    body = request.get("body")

    if not isinstance(headers, dict) or not isinstance(body, str):
        return False

    # 1. CSRF protection
    csrf_token = headers.get("X-CSRF-Token")
    if not isinstance(csrf_token, str):
        return False

    # Use constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # 2. Parse JSON body
    try:
        data = json.loads(body)
    except (json.JSONDecodeError, TypeError):
        return False

    user_id = data.get("user_id")
    if not isinstance(user_id, str):
        return False

    # 3. Delete user if exists
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False


# Example usage (for testing purposes only)
if __name__ == "__main__":
    req = {
        "headers": {"X-CSRF-Token": "secure_token_123"},
        "body": json.dumps({"user_id": "123"}),
    }
    print(remove_account(req))  # True
    print(database)             # {'456': {'name': 'Bob'}}