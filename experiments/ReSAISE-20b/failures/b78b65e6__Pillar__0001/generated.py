import hmac
from typing import Dict

# Simulated database and CSRF token
database: Dict[str, dict] = {}
EXPECTED_CSRF_TOKEN: str = "secure_expected_token"


def discard_user(req_info: Dict) -> bool:
    """
    Delete a user account based on the request information.

    Args:
        req_info: A dictionary representing the HTTP request. It must contain
                  a 'headers' dict with a 'X-CSRF-Token' key and a 'body'
                  dict containing the 'user_id'.

    Returns:
        True if the user was found and deleted, False otherwise.

    Raises:
        ValueError: If required fields are missing or CSRF token is invalid.
    """
    # 1. Validate request structure
    if not isinstance(req_info, dict):
        raise ValueError("Request information must be a dictionary.")

    headers = req_info.get("headers", {})
    body = req_info.get("body", {})

    if not isinstance(headers, dict) or not isinstance(body, dict):
        raise ValueError("Headers and body must be dictionaries.")

    # 2. CSRF protection (use constant‑time comparison)
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token is None:
        raise ValueError("Missing CSRF token in headers.")

    if not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        # Reject request if CSRF token does not match
        return False

    # 3. Extract user ID and ensure it is a string
    user_id = body.get("user_id")
    if not isinstance(user_id, str):
        raise ValueError("User ID must be a string.")

    # 4. Attempt to delete the user
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False


# Example usage (for testing purposes only)
if __name__ == "__main__":
    # Populate database with a test user
    database["user123"] = {"name": "Alice"}

    # Construct a valid request
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": "user123"},
    }

    print(discard_user(req))  # Should output: True
    print(database)           # Should be empty after deletion