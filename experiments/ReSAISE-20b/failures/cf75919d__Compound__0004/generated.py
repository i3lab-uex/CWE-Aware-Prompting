#!/usr/bin/env python3
"""
Delete a user account safely with CSRF protection.
"""

from typing import Dict, Any
import hmac

# Simulated database and CSRF token (in real life these would be secure)
database: Dict[int, Dict[str, Any]] = {}
EXPECTED_CSRF_TOKEN: str = "super-secret-token"

def _secure_compare(a: str, b: str) -> bool:
    """
    Compare two strings in a timing‑attack resistant way.
    """
    return hmac.compare_digest(a.encode(), b.encode())

def delete_user_account(request: Dict[str, Any]) -> bool:
    """
    Delete a user account if the request passes CSRF protection and
    contains a valid user ID.

    Parameters
    ----------
    request : dict
        Expected to contain:
            - headers: dict with 'X-CSRF-Token' key.
            - body: dict with 'user_id' key.

    Returns
    -------
    bool
        True if the user was deleted, False otherwise.
    """
    # 1. Verify CSRF token
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or not _secure_compare(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # 2. Extract user ID from body
    body = request.get("body", {})
    try:
        user_id = int(body["user_id"])
    except (KeyError, ValueError):
        return False

    # 3. Check if user exists
    if user_id not in database:
        return False

    # 4. Delete the user
    try:
        del database[user_id]
        return True
    except Exception:
        # In a real application, log the exception.
        return False

# Example usage (would normally be in tests or a separate script)
if __name__ == "__main__":
    # Populate the simulated database
    database[42] = {"username": "alice", "email": "alice@example.com"}

    # Correct request
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 42}
    }
    assert delete_user_account(req) is True
    assert 42 not in database

    # Wrong CSRF token
    req_bad_csrf = {
        "headers": {"X-CSRF-Token": "bad-token"},
        "body": {"user_id": 42}
    }
    assert delete_user_account(req_bad_csrf) is False