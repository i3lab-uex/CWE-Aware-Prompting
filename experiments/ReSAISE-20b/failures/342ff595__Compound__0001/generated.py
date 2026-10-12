import json
from typing import Dict, Any

# Mock in‑memory user database: {user_id: user_record}
database: Dict[str, Any] = {}

# Expected CSRF token value
EXPECTED_CSRF_TOKEN = "s3cureT0k3n"

def remove_user_profile(request_data: Dict[str, Any]) -> bool:
    """
    Remove a user profile from the mock database after validating CSRF token.

    Args:
        request_data: A dict representing an HTTP request. It must contain:
            - 'headers': a dict that includes the key 'X-CSRF-Token'
            - 'body': a JSON string or dict that includes the key 'user_id'

    Returns:
        bool: True if deletion succeeded, False otherwise.

    Security Notes:
        - Validates the CSRF token from request headers.
        - Handles missing keys gracefully without raising exceptions.
    """
    # 1. Validate CSRF token
    headers = request_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract user_id from body
    body = request_data.get("body")
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            return False

    user_id = body.get("user_id") if isinstance(body, dict) else None
    if not user_id:
        return False

    # 3. Delete user from database if exists
    return database.pop(user_id, None) is not None