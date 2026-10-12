import json
from typing import Dict, Any

# Example global constants and database (would normally be imported or configured elsewhere)
EXPECTED_CSRF_TOKEN = "secure_csrf_token_123"
database: Dict[str, Any] = {
    # user_id : user_data
    "user1": {"name": "Alice"},
    "user2": {"name": "Bob"},
}


def terminate_user_account(request_data: Dict[str, Any]) -> bool:
    """
    Delete a user account based on the provided request data.

    Parameters
    ----------
    request_data : dict
        A dictionary representing an HTTP request, expected to contain:
            - 'headers': a mapping with key 'X-CSRF-Token'
            - 'body': a JSON string or dict containing the key 'user_id'

    Returns
    -------
    bool
        True if deletion succeeded, False otherwise.
    """
    # 1. Validate CSRF token
    headers = request_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid or missing CSRF token
        return False

    # 2. Extract user_id from body
    body = request_data.get("body")
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            return False
    if not isinstance(body, dict) or "user_id" not in body:
        return False

    user_id = body["user_id"]

    # 3. Delete the user if it exists
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False