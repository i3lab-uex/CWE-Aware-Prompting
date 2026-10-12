import json
from typing import Dict

# Simulated database and CSRF token for demonstration purposes
database: Dict[int, dict] = {}
EXPECTED_CSRF_TOKEN = "expected_csrf_token_value"


def discard_user(req_info: Dict) -> bool:
    """
    Delete a user account from the simulated database.

    Args:
        req_info (dict): HTTP request information containing headers and body.
            Expected keys:
                - "headers": dict with a "X-CSRF-Token" key.
                - "body": JSON string containing the user ID, e.g. {"user_id": 42}.

    Returns:
        bool: True if the user was deleted, False otherwise.

    Raises:
        ValueError: If required fields are missing or malformed.
    """
    # 1. CSRF protection
    headers = req_info.get("headers")
    if not isinstance(headers, dict):
        raise ValueError("Missing or invalid headers")

    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Reject request due to CSRF token mismatch
        return False

    # 2. Extract user ID from request body
    body = req_info.get("body")
    if not isinstance(body, str):
        raise ValueError("Missing or invalid body")

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        raise ValueError("Body is not valid JSON")

    user_id = data.get("user_id")
    if not isinstance(user_id, int):
        raise ValueError("User ID must be an integer")

    # 3. Delete the user from the database
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False


# Example usage (for testing purposes only)
if __name__ == "__main__":
    # Populate the database with a sample user
    database[42] = {"name": "Alice"}

    # Simulate a request to delete user 42
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": json.dumps({"user_id": 42}),
    }

    result = discard_user(request)
    print("Deletion successful:", result)  # Expected: True