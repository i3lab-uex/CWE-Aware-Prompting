import json

# Constants and mock database
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"
database = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    # ... other users
}

def remove_user_account(req: dict) -> bool:
    """
    Remove a user account based on the user ID provided in the request.

    Args:
        req (dict): A representation of an HTTP request containing headers
                    and a JSON body with the user ID.

    Returns:
        bool: True if the account was removed successfully, False otherwise.
    """
    # Validate CSRF token
    csrf_token = req.get("headers", {}).get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid CSRF token – reject the request
        return False

    # Parse user ID from the body (JSON string)
    try:
        body = req.get("body", "{}")
        data = json.loads(body) if isinstance(body, str) else body
        user_id = int(data.get("user_id"))
    except (ValueError, TypeError, json.JSONDecodeError):
        # Malformed body or missing user_id
        return False

    # Remove the user from the database if it exists
    if user_id in database:
        del database[user_id]
        return True

    # User ID not found
    return False