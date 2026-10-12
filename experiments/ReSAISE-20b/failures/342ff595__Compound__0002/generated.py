import hashlib
from typing import Dict

# Constants and mock database
EXPECTED_CSRF_TOKEN = "secure_csrf_token_12345"
database: Dict[str, dict] = {
    "user1": {"name": "Alice", "email": "alice@example.com"},
    "user2": {"name": "Bob", "email": "bob@example.com"},
}


def _is_valid_csrf(token: str) -> bool:
    """
    Validate the CSRF token using a constant-time comparison to mitigate timing attacks.
    """
    if not isinstance(token, str):
        return False
    # Use hashlib.compare_digest for constant-time comparison
    return hashlib.compare_digest(token, EXPECTED_CSRF_TOKEN)


def remove_user_profile(request_data: Dict) -> bool:
    """
    Remove a user profile from the mock database.

    Parameters
    ----------
    request_data : dict
        A dictionary containing at least:
            - 'headers': dict, may include 'X-CSRF-Token'
            - 'body': dict, must contain 'user_id'

    Returns
    -------
    bool
        True if the user was successfully removed, False otherwise.
    """
    # Extract CSRF token from headers
    headers = request_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")

    # Validate CSRF token
    if not _is_valid_csrf(csrf_token):
        return False

    # Extract user_id from body
    body = request_data.get("body", {})
    user_id = body.get("user_id")

    if not isinstance(user_id, str):
        return False

    # Delete the user if present
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False


# Example usage (for testing purposes only)
if __name__ == "__main__":
    # Successful deletion
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": "user1"},
    }
    print(remove_user_profile(req))  # True

    # Attempt with wrong CSRF token
    req_bad_csrf = {
        "headers": {"X-CSRF-Token": "bad_token"},
        "body": {"user_id": "user2"},
    }
    print(remove_user_profile(req_bad_csrf))  # False

    # Attempt to delete non-existent user
    req_nonexistent = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": "nonexistent"},
    }
    print(remove_user_profile(req_nonexistent))  # False