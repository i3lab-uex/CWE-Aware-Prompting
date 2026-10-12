#!/usr/bin/env python3
"""
delete_user_account implementation.

The function removes a user from the simulated database after performing
basic validation checks:
  * CSRF token verification
  * User ID type and format check
  * Existence of the user in the database

If all checks pass, the user is deleted and True is returned.
Otherwise, False is returned.
"""

from __future__ import annotations

import re
from typing import Dict, Any


# Simulated database: mapping from user_id (str) to user data
database: Dict[str, Dict[str, Any]] = {
    "123": {"name": "Alice", "email": "alice@example.com"},
    "456": {"name": "Bob",   "email": "bob@example.com"},
}

# Expected CSRF token for this operation
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token-123"


def _is_valid_user_id(user_id: Any) -> bool:
    """
    Basic validation for user IDs.
    Accepts only non-empty strings composed of digits (i.e., numeric IDs).
    """
    if not isinstance(user_id, str):
        return False
    return bool(re.fullmatch(r"\d+", user_id))


def delete_user_account(request: Dict[str, Any]) -> bool:
    """
    Delete a user account from the simulated database.

    Parameters
    ----------
    request : dict
        The request object containing:
            - headers: dict (must contain 'X-CSRF-Token')
            - body   : dict (must contain 'user_id')

    Returns
    -------
    bool
        True if the user was successfully deleted, False otherwise.
    """
    # 1. CSRF token check
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract and validate user ID
    body = request.get("body", {})
    user_id = body.get("user_id")
    if not _is_valid_user_id(user_id):
        return False

    # 3. Check existence and delete
    if user_id not in database:
        return False

    try:
        del database[user_id]
        return True
    except Exception:
        # In a real application, log the exception.
        return False


# Example usage (for manual testing)
if __name__ == "__main__":
    test_request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body":   {"user_id": "123"},
    }
    print("Before deletion:", database)
    result = delete_user_account(test_request)
    print("Deletion successful?", result)
    print("After deletion:", database)