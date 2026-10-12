import json
from typing import Dict, Any

# Expected CSRF token constant (for example purposes)
EXPECTED_CSRF_TOKEN = "secure_csrf_token_123"

def remove_user_data(
    data: Dict[str, Any], database: Dict[int, Dict[str, Any]]
) -> bool:
    """
    Remove a user from the in-memory `database` based on the user ID provided
    in the request data. The function performs CSRF token validation and
    basic type checking before attempting deletion.

    Args:
        data: A dictionary representing an HTTP request. Expected keys:
            - "headers": dict containing a "X-CSRF-Token" entry.
            - "body": str or dict. If str, it must be JSON with a "user_id" key.
        database: A dict mapping user IDs (int) to user data dictionaries.

    Returns:
        True if the user was successfully removed, False otherwise.
    """
    # Validate headers and CSRF token
    try:
        headers = data.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            return False
    except Exception:
        # Malformed headers or missing CSRF token
        return False

    # Extract user ID from body
    try:
        body = data.get("body")
        if isinstance(body, str):
            body_dict = json.loads(body)
        elif isinstance(body, dict):
            body_dict = body
        else:
            return False

        user_id_raw = body_dict.get("user_id")
        if not isinstance(user_id_raw, int):
            return False
    except Exception:
        # Invalid JSON or missing user_id
        return False

    # Perform deletion in a thread‑safe manner if needed (not required for dict)
    return database.pop(user_id_raw, None) is not None