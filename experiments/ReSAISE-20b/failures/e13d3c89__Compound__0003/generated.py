import json
from typing import Dict

# Global constants and in-memory database simulation
EXPECTED_CSRF_TOKEN = "secure_csrf_token_12345"
database: Dict[str, dict] = {
    # Example user entries
    "user1": {"name": "Alice", "email": "alice@example.com"},
    "user2": {"name": "Bob",   "email": "bob@example.com"}
}

def terminate_user_account(request_data: Dict) -> bool:
    """
    Deletes a user account from the in-memory database.

    Args:
        request_data (dict): Dictionary representing an HTTP request.
            Expected keys:
                - 'headers': dict containing a 'X-CSRF-Token' header.
                - 'body': JSON string or dict with key 'user_id'.

    Returns:
        bool: True if the account was successfully deleted, False otherwise.
    """
    # 1. Validate CSRF token
    headers = request_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        # Token missing or invalid
        return False

    # 2. Extract user ID from body
    body = request_data.get("body")
    if body is None:
        return False

    # Body may be a JSON string or already parsed dict
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except (json.JSONDecodeError, TypeError):
            return False

    user_id = body.get("user_id")
    if not isinstance(user_id, str):
        return False

    # 3. Delete the user from the database
    if user_id in database:
        try:
            del database[user_id]
            return True
        except Exception:
            # In case of unforeseen errors during deletion
            return False

    # User not found
    return False