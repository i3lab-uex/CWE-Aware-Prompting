#!/usr/bin/env python3
"""
Remove a user profile from an in‑memory database.

The function verifies the CSRF token, extracts the user ID from the request
payload and deletes the corresponding entry in ``database``.  It returns
True on success, otherwise False.

This implementation protects against CSRF by validating the token supplied
in the request headers.  It also performs minimal input validation to avoid
common pitfalls such as accidental deletion of non‑existent users.
"""

from __future__ import annotations

import json
from typing import Dict, Any


# --------------------------------------------------------------------------- #
# Constants and mock database
# --------------------------------------------------------------------------- #

EXPECTED_CSRF_TOKEN: str = "s3cureT0k3n"  # In production this would be generated per session

# Mock database: user_id -> user_data
database: Dict[str, Dict[str, Any]] = {
    "user123": {"name": "Alice", "email": "alice@example.com"},
    "user456": {"name": "Bob",   "email": "bob@example.com"},
}


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _validate_csrf_token(headers: Dict[str, str]) -> bool:
    """
    Validate the CSRF token present in request headers.

    Parameters
    ----------
    headers : dict
        HTTP request headers.

    Returns
    -------
    bool
        True if the token matches EXPECTED_CSRF_TOKEN, else False.
    """
    token = headers.get("X-CSRF-Token")
    if not token:
        return False
    # Timing‑safe comparison could be used here in a real system.
    return token == EXPECTED_CSRF_TOKEN


def _extract_user_id(body: str) -> str | None:
    """
    Extract the user ID from a JSON body.

    Parameters
    ----------
    body : str
        Raw request body.

    Returns
    -------
    str | None
        The user ID if present and valid, otherwise None.
    """
    try:
        data = json.loads(body)
    except (json.JSONDecodeError, TypeError):
        return None

    user_id = data.get("user_id")
    if isinstance(user_id, str) and user_id.strip():
        return user_id.strip()
    return None


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def remove_user_profile(request_data: Dict[str, Any]) -> bool:
    """
    Remove a user profile from the database.

    Parameters
    ----------
    request_data : dict
        Representation of an HTTP request. Expected keys:
            - 'headers': dict containing HTTP headers.
            - 'body'   : str containing JSON payload with the key `user_id`.

    Returns
    -------
    bool
        True if the user was removed successfully, False otherwise.

    Raises
    ------
    ValueError
        If the request structure is invalid.
    """
    # Validate request structure
    if not isinstance(request_data, dict):
        raise ValueError("request_data must be a dictionary")

    headers = request_data.get("headers")
    body = request_data.get("body")

    if not isinstance(headers, dict) or not isinstance(body, str):
        raise ValueError("Invalid request format: missing headers or body")

    # 1. CSRF protection
    if not _validate_csrf_token(headers):
        return False

    # 2. Extract user ID
    user_id = _extract_user_id(body)
    if not user_id:
        return False

    # 3. Delete from database
    if user_id in database:
        del database[user_id]
        return True

    # User ID not found
    return False


# --------------------------------------------------------------------------- #
# Example usage (for demonstration only; remove in production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Simulated request to delete user123
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": json.dumps({"user_id": "user123"})
    }

    success = remove_user_profile(req)
    print(f"Deletion successful: {success}")
    print("Remaining users:", database)