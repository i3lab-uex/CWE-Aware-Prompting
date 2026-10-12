#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A simple function that updates a user's phone number in an in‑memory database.
It validates the CSRF token, checks that the user exists and that the new phone
number is syntactically valid.  The function returns ``True`` on success and
``False`` otherwise.
"""

import re
from typing import Dict

# Sample in‑memory user database (user_id -> dict of attributes)
database: Dict[str, Dict] = {
    "1": {"name": "Alice", "phone": "+15551234567"},
    "2": {"name": "Bob",   "phone": "+15559876543"},
}

# Pre‑configured CSRF token that the client must supply
EXPECTED_CSRF_TOKEN: str = "a1b2c3d4e5f6g7h8i9j0"

# Regular expression for a basic E.164 phone number format
PHONE_REGEX = re.compile(r"^\+[1-9]\d{1,14}$")


def _is_valid_csrf_token(token: str) -> bool:
    """
    Validate the CSRF token.  Use a constant‑time comparison to avoid timing attacks.
    """
    if not isinstance(token, str):
        return False
    # Simple constant‑time comparison (works for short strings)
    if len(token) != len(EXPECTED_CSRF_TOKEN):
        return False
    result = 0
    for x, y in zip(token, EXPECTED_CSRF_TOKEN):
        result |= ord(x) ^ ord(y)
    return result == 0


def _is_valid_phone(phone: str) -> bool:
    """
    Validate that the phone number matches E.164 format.
    """
    return isinstance(phone, str) and PHONE_REGEX.fullmatch(phone) is not None


def modify_user_phone(user_request: Dict) -> bool:
    """
    Update a user's phone number after validating CSRF token and input data.

    Parameters
    ----------
    user_request : dict
        Dictionary containing request headers and body.  Expected keys:
            - "headers": dict, must contain a "X-CSRF-Token" entry
            - "body": dict, must contain "user_id" and "new_phone"

    Returns
    -------
    bool
        ``True`` if the phone number was successfully updated, otherwise ``False``.

    Notes
    -----
    - The function performs minimal checks to avoid leaking information.
    - It does not raise exceptions on invalid input; it simply returns ``False``.
    """
    try:
        headers = user_request.get("headers", {})
        body = user_request.get("body", {})

        csrf_token = headers.get("X-CSRF-Token")
        if not _is_valid_csrf_token(csrf_token):
            return False

        user_id = body.get("user_id")
        new_phone = body.get("new_phone")

        if not (isinstance(user_id, str) and isinstance(new_phone, str)):
            return False

        if not _is_valid_phone(new_phone):
            return False

        user_record = database.get(user_id)
        if not user_record:
            return False

        # Perform the update
        user_record["phone"] = new_phone
        return True

    except Exception:
        # Catch unexpected errors to avoid leaking stack traces
        return False


# Example usage (for manual testing only)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": "1", "new_phone": "+15551230000"},
    }
    print("Update success:", modify_user_phone(request))
    print("Updated record:", database["1"])