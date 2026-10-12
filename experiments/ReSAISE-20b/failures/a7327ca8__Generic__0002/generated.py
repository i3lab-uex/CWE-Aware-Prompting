import json
from typing import Dict, Any

# Simulated database (to be provided in the calling context)
database: Dict[str, Any] = {}

# Expected CSRF token for verification
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_value"


def remove_account(request: Dict[str, Any]) -> bool:
    """
    Deletes a user account from the simulated database.

    Args:
        request: A dictionary representing an HTTP request. It must contain
                 a 'headers' key with a dict of headers and a 'body' key
                 containing JSON data that includes the user ID.

    Returns:
        True if the account was deleted successfully, False otherwise.
    """
    # 1. Validate request structure
    if not isinstance(request, dict):
        return False

    headers = request.get("headers")
    body_raw = request.get("body")

    if not isinstance(headers, dict) or not isinstance(body_raw, (str, bytes)):
        return False

    # 2. CSRF protection
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 3. Parse body JSON
    try:
        body = json.loads(body_raw if isinstance(body_raw, str) else body_raw.decode())
    except (json.JSONDecodeError, AttributeError):
        return False

    # 4. Extract user ID
    user_id = body.get("user_id")
    if not isinstance(user_id, str):
        return False

    # 5. Delete user from database
    try:
        if user_id in database:
            del database[user_id]
            return True
        else:
            # User does not exist; consider this a failure to delete
            return False
    except Exception:
        # Any unexpected error during deletion should result in a failure.
        return False