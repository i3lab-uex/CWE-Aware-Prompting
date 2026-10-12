#!/usr/bin/env python3
"""
remove_user_account.py

This module provides a single function `remove_user_account` which removes
a user entry from an in‑memory database after verifying a CSRF token.
"""

from __future__ import annotations

import typing as _t


# --------------------------------------------------------------------------- #
# Configuration / context
# --------------------------------------------------------------------------- #

# Simulated in‑memory database: {user_id: user_data}
database: dict[int, _t.Any] = {}

# Predefined CSRF token that must match the request header
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token-12345"


# --------------------------------------------------------------------------- #
# Utility functions
# --------------------------------------------------------------------------- #

def _is_valid_csrf(token: str | None) -> bool:
    """
    Validate the CSRF token.

    Parameters
    ----------
    token : str | None
        The token extracted from the request header.

    Returns
    -------
    bool
        True if the token matches EXPECTED_CSRF_TOKEN, False otherwise.
    """
    return isinstance(token, str) and token == EXPECTED_CSRF_TOKEN


def _extract_user_id(body: dict | None) -> int | None:
    """
    Extract the user ID from the request body.

    Parameters
    ----------
    body : dict | None
        The parsed JSON body of the request.

    Returns
    -------
    int | None
        The user ID if present and an integer, otherwise None.
    """
    if not isinstance(body, dict):
        return None
    user_id = body.get("user_id")
    if isinstance(user_id, int) and user_id >= 0:
        return user_id
    return None


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def remove_user_account(input_request: dict) -> bool:
    """
    Delete a user account from the in-memory database after CSRF validation.

    Parameters
    ----------
    input_request : dict
        Dictionary representing an HTTP request. Expected keys:
            - 'headers': dict containing a 'X-CSRF-Token' key.
            - 'body': dict containing the user ID under 'user_id'.

    Returns
    -------
    bool
        True if the account was deleted, False otherwise.

    Notes
    -----
    - The function is deliberately defensive: it checks the presence and types of
      all required fields before proceeding.
    - If the user ID does not exist in `database`, deletion is considered a
      failure and False is returned.
    - No exception is raised; all errors are handled gracefully.
    """
    # Basic request structure validation
    if not isinstance(input_request, dict):
        return False

    headers = input_request.get("headers")
    body = input_request.get("body")

    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # CSRF token validation
    csrf_token = headers.get("X-CSRF-Token")
    if not _is_valid_csrf(csrf_token):
        return False

    # Extract and validate user ID
    user_id = _extract_user_id(body)
    if user_id is None:
        return False

    # Delete the user from the database
    try:
        if user_id in database:
            del database[user_id]
            return True
        else:
            # User does not exist
            return False
    except Exception:
        # Catch unexpected errors (e.g., concurrent modifications)
        return False


# --------------------------------------------------------------------------- #
# Example usage / test harness (uncomment to run directly)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Populate database with a sample user
    database[42] = {"name": "Alice"}

    # Build a request to delete that user
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 42}
    }

    print("Before deletion:", database)
    result = remove_user_account(req)
    print("Deletion successful?", result)
    print("After deletion:", database)