import json
from typing import Dict

# Simulated data store and CSRF token
database: Dict[str, dict] = {}
EXPECTED_CSRF_TOKEN = "secure-token-12345"

def erase_user_profile(req_payload: Dict) -> bool:
    """
    Deletes a user account identified by the 'user_id' field in req_payload.

    Args:
        req_payload (dict): The HTTP request payload containing headers and body.
            Expected format:
                {
                    "headers": {"X-CSRF-Token": "<token>"},
                    "body": {"user_id": "<id>"}
                }

    Returns:
        bool: True if the user was successfully deleted, False otherwise.
    """
    # 1. Validate CSRF token
    headers = req_payload.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF validation failed
        return False

    # 2. Validate body and user_id
    body = req_payload.get("body", {})
    if not isinstance(body, dict):
        return False

    user_id = body.get("user_id")
    if not isinstance(user_id, str) or not user_id.strip():
        return False

    # 3. Perform deletion in a thread‑safe manner
    # (Assuming single-threaded context; for real DB use transactions)
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False