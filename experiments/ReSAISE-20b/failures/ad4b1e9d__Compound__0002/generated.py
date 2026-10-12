import json
from typing import Dict, Any

# Simulated database and CSRF token for the purpose of this example
database: Dict[str, Any] = {}
EXPECTED_CSRF_TOKEN: str = "secure_token_123"

def erase_user_profile(req_payload: Dict[str, Any]) -> bool:
    """
    Delete a user profile from the database.

    Parameters
    ----------
    req_payload : dict
        HTTP request representation containing:
            - 'headers': dict of request headers.
            - 'body'   : JSON string or dict with a 'user_id' key.

    Returns
    -------
    bool
        True if the user was found and deleted, False otherwise.

    Raises
    ------
    ValueError
        If required fields are missing or the CSRF token is invalid.
    """
    # Validate headers
    headers = req_payload.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Headers must be a dictionary")

    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token:
        raise ValueError("Missing CSRF token in headers")

    # Check CSRF protection (CWE-352 mitigation)
    if csrf_token != EXPECTED_CSRF_TOKEN:
        raise ValueError("Invalid CSRF token")

    # Extract body
    body = req_payload.get("body")
    if body is None:
        raise ValueError("Missing request body")

    # Body might be a JSON string or already parsed dict
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            raise ValueError("Body is not valid JSON")

    if not isinstance(body, dict):
        raise ValueError("Body must be a dictionary after parsing")

    user_id = body.get("user_id")
    if not user_id:
        raise ValueError("Missing 'user_id' in request body")

    # Delete the user if present
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False