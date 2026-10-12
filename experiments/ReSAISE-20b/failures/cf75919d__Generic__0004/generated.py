#!/usr/bin/env python3
"""
Utility to delete a user account from a simulated database.
"""

from __future__ import annotations

import json
from typing import Dict, Any

# Simulated database (global context)
database: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
}

# Expected CSRF token (would normally come from config or environment)
EXPECTED_CSRF_TOKEN = "secure_csrf_token_123"


def delete_user_account(request: Dict[str, Any]) -> bool:
    """
    Delete a user account based on the request payload.

    Parameters
    ----------
    request : dict
        A dictionary representing an HTTP request. Expected keys:
            - 'headers': mapping of header names to values.
            - 'body'   : JSON string or dict containing the user ID.

    Returns
    -------
    bool
        True if deletion succeeded, False otherwise.

    Notes
    -----
    - Performs CSRF token validation.
    - Expects user ID to be an integer.
    - Handles missing or malformed data gracefully.
    """
    # 1. Validate CSRF token
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract user ID from body
    raw_body = request.get("body")
    if raw_body is None:
        return False

    # Body may be a JSON string or already parsed dict
    if isinstance(raw_body, str):
        try:
            body = json.loads(raw_body)
        except (json.JSONDecodeError, TypeError):
            return False
    elif isinstance(raw_body, dict):
        body = raw_body
    else:
        return False

    user_id_raw = body.get("user_id")
    if user_id_raw is None:
        return False

    # Ensure user_id is an integer
    try:
        user_id = int(user_id_raw)
    except (ValueError, TypeError):
        return False

    # 3. Delete user from database if exists
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False


# Example usage (for testing purposes only)
if __name__ == "__main__":
    # Successful deletion
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": json.dumps({"user_id": 1}),
    }
    print(delete_user_account(req))  # True

    # Attempt to delete non-existent user
    req["body"] = json.dumps({"user_id": 999})
    print(delete_user_account(req))  # False

    # Invalid CSRF token
    req["headers"]["X-CSRF-Token"] = "bad_token"
    print(delete_user_account(req))  # False