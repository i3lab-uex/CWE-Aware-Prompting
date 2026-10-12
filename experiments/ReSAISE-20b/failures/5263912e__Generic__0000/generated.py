# -*- coding: utf-8 -*-
"""
A simple module that provides a function to remove a user account from an
in‑memory database.  The implementation focuses on safety checks such as
CSRF validation, input type checking and graceful failure handling.
"""

from __future__ import annotations

from typing import Dict, Any


# --------------------------------------------------------------------------- #
# Mock in‑memory database and CSRF token constant
# --------------------------------------------------------------------------- #

# Example structure: {user_id (int): user_record (dict)}
database: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
}

# The expected CSRF token that must be supplied in the request headers.
EXPECTED_CSRF_TOKEN: str = "s3cr3t-csrf-token"


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #

def _validate_csrf_token(token: str | None) -> bool:
    """
    Validate the CSRF token.

    Parameters
    ----------
    token : str | None
        The token supplied in the request headers.

    Returns
    -------
    bool
        ``True`` if the token matches ``EXPECTED_CSRF_TOKEN``, otherwise
        ``False``.
    """
    return token == EXPECTED_CSRF_TOKEN


def _extract_user_id(body: Dict[str, Any]) -> int | None:
    """
    Extract and validate the user ID from the request body.

    Parameters
    ----------
    body : dict
        The JSON payload of the HTTP request.

    Returns
    -------
    int | None
        The user ID if it is present and an integer, otherwise ``None``.
    """
    try:
        user_id = body.get("user_id")
        if isinstance(user_id, int):
            return user_id
    except AttributeError:
        # body is not a dict-like object
        pass
    return None


# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #

def remove_user_account(req: Dict[str, Any]) -> bool:
    """
    Remove a user account from the system based on the supplied request.

    The function performs several safety checks:
        1. CSRF token validation.
        2. User ID extraction and type checking.
        3. Existence check in the database.

    Parameters
    ----------
    req : dict
        A representation of an HTTP request containing:
            - ``headers`` (dict): request headers.
            - ``body``   (dict): JSON payload with the key ``user_id``.

    Returns
    -------
    bool
        ``True`` if the account was removed successfully, otherwise ``False``.

    Notes
    -----
    No exceptions are raised; failures are reported via the boolean return value.
    """
    # 1. CSRF protection
    headers = req.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not _validate_csrf_token(csrf_token):
        return False

    # 2. Extract and validate user ID
    body = req.get("body", {})
    user_id = _extract_user_id(body)
    if user_id is None:
        return False

    # 3. Attempt to delete the record
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False


# --------------------------------------------------------------------------- #
# Example usage (for testing purposes only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Successful removal
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1}
    }
    print(remove_user_account(request))   # Expected: True

    # Attempt to remove non‑existent user
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 999}
    }
    print(remove_user_account(request))   # Expected: False

    # CSRF failure
    request = {
        "headers": {"X-CSRF-Token": "wrong-token"},
        "body": {"user_id": 2}
    }
    print(remove_user_account(request))   # Expected: False