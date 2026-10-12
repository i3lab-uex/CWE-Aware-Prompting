#!/usr/bin/env python3
"""
Utility to update a user's phone number in a mock database.

This module demonstrates a safe CSRF token check, input validation,
and minimal error handling.  It is intentionally lightweight for
educational purposes and should not be used in production without
additional security hardening.
"""

from __future__ import annotations

import re
import hmac
import typing as _t

# --------------------------------------------------------------------------- #
# Configuration and mock database
# --------------------------------------------------------------------------- #

# Pre‑configured CSRF token (in a real app this would be stored securely)
EXPECTED_CSRF_TOKEN: str = "a1b2c3d4e5f6g7h8i9j0"

# Sample user database: {user_id (str): {"phone": str}}
database: dict[str, dict[str, str]] = {
    "user123": {"phone": "+15551234567"},
    "alice": {"phone": "+447700900123"},
}


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _is_valid_phone(phone: str) -> bool:
    """
    Validate that the phone number matches a simple E.164 pattern.
    This is intentionally permissive; real validation would be more complex.
    """
    return bool(re.fullmatch(r"\+[1-9]\d{7,15}", phone))


# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def alter_user_phone(service_request: dict) -> bool:
    """
    Update the phone number for a user based on a service request.

    Parameters
    ----------
    service_request : dict
        Expected to contain:
            headers: dict – must include 'X-CSRF-Token'
            body   : dict – must contain 'user_id' and 'new_phone'

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.
    """
    # --------------------------------------------------------------------- #
    # 1. CSRF token validation
    # --------------------------------------------------------------------- #
    headers: dict = service_request.get("headers", {})
    token: str | None = headers.get("X-CSRF-Token")

    if not isinstance(token, str):
        # Missing or non‑string token – fail fast
        return False

    # Use constant‑time comparison to avoid timing attacks (CWE-693)
    if not hmac.compare_digest(token, EXPECTED_CSRF_TOKEN):
        return False

    # --------------------------------------------------------------------- #
    # 2. Extract and validate request body
    # --------------------------------------------------------------------- #
    body: dict = service_request.get("body", {})
    if not isinstance(body, dict):
        return False

    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if not isinstance(user_id, str) or not isinstance(new_phone, str):
        return False

    # Basic phone number validation
    if not _is_valid_phone(new_phone):
        return False

    # --------------------------------------------------------------------- #
    # 3. Update the database
    # --------------------------------------------------------------------- #
    user_record = database.get(user_id)
    if not user_record:
        return False  # User does not exist

    # Perform the update
    user_record["phone"] = new_phone
    return True


# --------------------------------------------------------------------------- #
# Example usage (for testing purposes only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # A valid request
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": "alice", "new_phone": "+447700900999"},
    }
    print(alter_user_phone(req))  # Expected: True
    print(database["alice"]["phone"])  # Updated phone number

    # An invalid request (wrong token)
    bad_req = {
        "headers": {"X-CSRF-Token": "invalid"},
        "body": {"user_id": "alice", "new_phone": "+447700900999"},
    }
    print(alter_user_phone(bad_req))  # Expected: False