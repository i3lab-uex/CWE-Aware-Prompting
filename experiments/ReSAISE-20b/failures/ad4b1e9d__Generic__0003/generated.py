import json
from typing import Dict, Any

# These would normally be defined elsewhere in the application.
# They are referenced here for completeness of the example.
database: Dict[str, Any] = {}  # key: user_id, value: user data
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token"

def erase_user_profile(req_payload: Dict[str, Any]) -> bool:
    """
    Delete a user account based on the incoming request payload.

    Parameters
    ----------
    req_payload : dict
        The HTTP request representation containing:
            - 'headers': dict with at least a 'X-CSRF-Token' key
            - 'body': JSON string or dict containing the user ID under 'user_id'

    Returns
    -------
    bool
        True if deletion succeeded, False otherwise.
    """
    # Validate request structure
    if not isinstance(req_payload, dict):
        return False

    headers = req_payload.get("headers")
    body = req_payload.get("body")

    if not isinstance(headers, dict) or not isinstance(body, (dict, str)):
        return False

    # Verify CSRF token
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # Extract user ID from body
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except (json.JSONDecodeError, TypeError):
            return False

    user_id = body.get("user_id")
    if not isinstance(user_id, str) or not user_id:
        return False

    # Perform deletion atomically
    try:
        # Using pop ensures no KeyError if the user doesn't exist.
        deleted = database.pop(user_id, None)
    except Exception:
        # Any unexpected exception should not expose internal state
        return False

    return deleted is not None