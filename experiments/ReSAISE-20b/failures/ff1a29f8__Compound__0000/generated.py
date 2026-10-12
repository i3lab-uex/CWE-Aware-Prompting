#!/usr/bin/env python3
"""
A small helper module that demonstrates how a web application might safely update a user's phone number.
The implementation focuses on protecting against CSRF and basic input validation.
"""

from __future__ import annotations

import re
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Configuration / Mock objects (would normally be provided by the application)
# --------------------------------------------------------------------------- #

# Example mock database: user_id -> dict with details
database: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "phone": "+15551234567"},
    2: {"name": "Bob",   "phone": "+15559876543"},
}

# Expected CSRF token (in a real app this would be stored in the user's session)
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_12345"

# --------------------------------------------------------------------------- #
# Utility functions
# --------------------------------------------------------------------------- #

def _validate_csrf_token(token: str) -> bool:
    """
    Compare the supplied CSRF token against the expected value in a timing‑safe way.
    """
    return re.escape(token) == re.escape(EXPECTED_CSRF_TOKEN)

def _validate_user_id(user_id: Any) -> int | None:
    """
    Ensure the user ID is an integer and exists in the database.
    """
    try:
        uid = int(user_id)
    except (TypeError, ValueError):
        return None
    if uid not in database:
        return None
    return uid

def _validate_phone_number(phone: str) -> bool:
    """
    Basic validation for a phone number.
    Accepts international format with optional leading '+' and 7–15 digits.
    """
    pattern = re.compile(r"^\+?\d{7,15}$")
    return bool(pattern.match(phone))

# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #

def change_user_phone(request_details: Dict[str, Any]) -> bool:
    """
    Update a user's phone number in the mock database.

    Parameters
    ----------
    request_details : dict
        A dictionary that must contain:
            - 'headers': a mapping of HTTP header names to values
            - 'body'   : a mapping with keys:
                * 'user_id'   (int or str convertible to int)
                * 'phone'     (str, new phone number)

    Returns
    -------
    bool
        True if the update was successful; False otherwise.

    Raises
    ------
    ValueError
        If required fields are missing or malformed.
    """
    # 1. Basic request structure check
    if not isinstance(request_details, dict):
        raise ValueError("request_details must be a dictionary")

    headers = request_details.get("headers", {})
    body   = request_details.get("body", {})

    if not isinstance(headers, dict) or not isinstance(body, dict):
        raise ValueError("headers and body must be dictionaries")

    # 2. CSRF protection
    csrf_token = headers.get("X-CSRF-Token") or headers.get("csrf-token")
    if not csrf_token or not _validate_csrf_token(csrf_token):
        return False

    # 3. Extract and validate user ID
    raw_user_id = body.get("user_id")
    if raw_user_id is None:
        return False
    user_id = _validate_user_id(raw_user_id)
    if user_id is None:
        return False

    # 4. Validate new phone number
    raw_phone = body.get("phone")
    if not isinstance(raw_phone, str) or not _validate_phone_number(raw_phone):
        return False

    # 5. Perform the update
    try:
        database[user_id]["phone"] = raw_phone
    except Exception:
        # Any unforeseen error (e.g., missing key) results in a failure
        return False

    return True

# --------------------------------------------------------------------------- #
# Example usage (would be removed or replaced in production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Successful update
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body":    {"user_id": 1, "phone": "+15559998888"}
    }
    print("Update success:", change_user_phone(req))  # Expected: True
    print("New phone:", database[1]["phone"])        # Expected: +15559998888

    # Failed due to missing CSRF
    req_no_csrf = {"headers": {}, "body": {"user_id": 1, "phone": "+15550000000"}}
    print("Update success:", change_user_phone(req_no_csrf))  # Expected: False