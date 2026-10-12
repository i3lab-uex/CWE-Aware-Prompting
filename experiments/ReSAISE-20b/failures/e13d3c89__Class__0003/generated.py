import uuid
from typing import Dict

# ------------------------------------------------------------------
# Configuration and mock database (in‑memory)
# ------------------------------------------------------------------

EXPECTED_CSRF_TOKEN = "secure-expected-token"

# Example in‑memory user database
database: Dict[str, dict] = {
    "user-1": {"name": "Alice", "email": "alice@example.com"},
    "user-2": {"name": "Bob",   "email": "bob@example.com"},
}

# ------------------------------------------------------------------
# Helper utilities
# ------------------------------------------------------------------

def _is_valid_user_id(user_id: str) -> bool:
    """
    Basic validation for user IDs. For this example we assume
    user IDs are UUID4 strings.
    """
    try:
        uuid_obj = uuid.UUID(user_id, version=4)
    except (ValueError, AttributeError):
        return False
    # Ensure the string representation matches the original input
    return str(uuid_obj) == user_id

def _verify_csrf_token(token: str) -> bool:
    """
    Verify that the provided CSRF token matches the expected value.
    The comparison is performed in constant time to avoid timing attacks.
    """
    if not isinstance(token, str):
        return False
    # Use a constant‑time comparison
    if len(token) != len(EXPECTED_CSRF_TOKEN):
        return False
    result = 0
    for x, y in zip(token.encode(), EXPECTED_CSRF_TOKEN.encode()):
        result |= x ^ y
    return result == 0

# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------

def terminate_user_account(request_data: Dict) -> bool:
    """
    Deletes a user account based on the provided request data.

    Parameters
    ----------
    request_data : dict
        Expected to contain:
            - headers: dict with key 'X-CSRF-Token' for CSRF protection
            - body: dict containing 'user_id' key

    Returns
    -------
    bool
        True if the account was deleted, False otherwise.
    """
    # 1. CSRF token validation
    headers = request_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not _verify_csrf_token(csrf_token):
        return False

    # 2. Extract and validate user ID
    body = request_data.get("body", {})
    user_id = body.get("user_id")
    if not isinstance(user_id, str) or not _is_valid_user_id(user_id):
        return False

    # 3. Delete the user if present
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False

# ------------------------------------------------------------------
# Example usage (for testing purposes)
# ------------------------------------------------------------------

if __name__ == "__main__":
    # Create a valid UUID4 user ID
    new_user_id = str(uuid.uuid4())
    database[new_user_id] = {"name": "Charlie", "email": "charlie@example.com"}

    # Build request data
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": new_user_id}
    }

    # Attempt deletion
    result = terminate_user_account(req)
    print(f"Deletion successful: {result}")   # Expected: True