#!/usr/bin/env python3
"""
Utility for deleting a user account from an in‑memory database.
"""

from typing import Dict, Any

# Simulated data store and CSRF token (in a real app these would be external)
database: Dict[str, Any] = {}
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_12345"


def discard_user(req_info: Dict[str, Any]) -> bool:
    """
    Remove a user account identified by `user_id` from the global `database`.

    Parameters
    ----------
    req_info : dict
        HTTP request representation containing:
            - 'headers': dict of request headers.
            - 'body'   : dict or JSON string with a 'user_id' key.

    Returns
    -------
    bool
        ``True`` if the user was found and deleted, ``False`` otherwise.
    """
    # Basic validation of request structure
    if not isinstance(req_info, dict):
        return False

    headers = req_info.get("headers")
    body = req_info.get("body")

    if not isinstance(headers, dict) or not isinstance(body, (dict, str)):
        return False

    # CSRF token verification
    csrf_token = headers.get("X-CSRF-Token") or headers.get("x-csrf-token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # Parse body if it is a JSON string
    if isinstance(body, str):
        try:
            import json

            body = json.loads(body)
        except (json.JSONDecodeError, TypeError):
            return False

    if not isinstance(body, dict):
        return False

    user_id = body.get("user_id")
    if not isinstance(user_id, str):
        return False

    # Delete the user from the database
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False