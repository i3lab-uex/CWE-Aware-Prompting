import uuid
from typing import Dict, Any

# Simulated data store and CSRF token
database: Dict[str, Dict[str, Any]] = {}
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token-12345"


def remove_account(request: Dict[str, Any]) -> bool:
    """
    Remove a user account from the simulated database.

    Parameters
    ----------
    request : dict
        HTTP request representation containing:
            - 'headers': dict, may include 'X-CSRF-Token'
            - 'body'   : dict, must contain 'user_id'

    Returns
    -------
    bool
        True if the account was deleted, False otherwise.
    """
    # Basic validation of request structure
    headers = request.get("headers", {})
    body = request.get("body", {})

    # CSRF protection
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # Extract user ID and validate format
    user_id = body.get("user_id")
    if not isinstance(user_id, str):
        return False

    # Ensure the user ID exists in the database
    if user_id not in database:
        return False

    # Perform deletion
    try:
        del database[user_id]
        return True
    except Exception:
        # In a real system, log the exception details securely
        return False


# Example usage (for testing purposes only)
if __name__ == "__main__":
    # Populate database with a sample user
    uid = str(uuid.uuid4())
    database[uid] = {"name": "Alice", "email": "alice@example.com"}

    # Construct a valid request
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": uid}
    }

    print(remove_account(req))  # Expected: True
    print(uid in database)      # Expected: False