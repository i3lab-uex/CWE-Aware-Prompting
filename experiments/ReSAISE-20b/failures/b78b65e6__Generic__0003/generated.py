import json
from typing import Dict

# Simulated database and CSRF token (normally these would be configured elsewhere)
database: Dict[str, dict] = {
    "1": {"name": "Alice"},
    "2": {"name": "Bob"},
}
EXPECTED_CSRF_TOKEN = "secure_csrf_token_123"

def discard_user(req_info: Dict) -> bool:
    """
    Remove a user account from the simulated database.

    Parameters
    ----------
    req_info : dict
        Dictionary representing an HTTP request. Expected keys:
            - 'headers': mapping of header names to values
            - 'body': raw request body (bytes or str)

    Returns
    -------
    bool
        True if the user was successfully deleted, False otherwise.
    """
    # 1. Validate CSRF token
    headers = req_info.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token") or headers.get("csrf-token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid CSRF token
        return False

    # 2. Parse body to extract user_id
    body = req_info.get("body")
    if not body:
        return False

    # Body may be bytes or str; ensure string
    if isinstance(body, bytes):
        try:
            body = body.decode("utf-8")
        except UnicodeDecodeError:
            return False

    # Try JSON first
    user_id = None
    try:
        data = json.loads(body)
        if isinstance(data, dict):
            user_id = str(data.get("user_id") or data.get("id"))
    except json.JSONDecodeError:
        # Fallback: simple form-encoded data
        for part in body.split("&"):
            if "=" not in part:
                continue
            key, val = part.split("=", 1)
            if key in ("user_id", "id"):
                user_id = val
                break

    if not user_id:
        return False  # No user ID provided

    # 3. Delete the user from the database if present
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False