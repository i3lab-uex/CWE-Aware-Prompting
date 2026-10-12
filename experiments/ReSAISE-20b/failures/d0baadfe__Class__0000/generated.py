#!/usr/bin/env python3
"""
Utility to modify a user's phone number in an in‑memory database.

The function validates the CSRF token, parses and sanitises input,
and updates the phone number only if the user exists.

Security notes:
- CSRF token is verified before any database operation.
- Input values are validated for type and format to prevent
  injection or malformed data.
- The database is a simple dictionary; in production this would be
  replaced by an ORM or parameterised SQL queries.
"""

from __future__ import annotations

import re
from typing import Dict, Any


# Sample in‑memory database: user_id -> user record dict
database: Dict[str, Dict[str, Any]] = {
    "123": {"name": "Alice", "phone": "+15551234567"},
    "456": {"name": "Bob",   "phone": "+15557654321"},
}

# Pre‑configured CSRF token for validation
EXPECTED_CSRF_TOKEN = "a1b2c3d4e5f6g7h8"


def _is_valid_phone_number(phone: str) -> bool:
    """
    Very basic phone number validation.
    Accepts digits, optional leading '+', and length 7–15.
    """
    return bool(re.fullmatch(r"\+?\d{7,15}", phone))


def modify_user_phone(user_request: Dict[str, Any]) -> bool:
    """
    Modify the phone number of a user.

    Parameters
    ----------
    user_request : dict
        Dictionary containing 'headers' and 'body'.  The body must include:
            - user_id : str
            - new_phone : str

    Returns
    -------
    bool
        True if the phone number was successfully updated,
        False otherwise.
    """
    # 1. CSRF token verification
    headers = user_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Token mismatch: reject the request
        return False

    # 2. Extract and validate body data
    body = user_request.get("body", {})
    if not isinstance(body, dict):
        return False

    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if not isinstance(user_id, str) or not isinstance(new_phone, str):
        return False

    # 3. Sanitize input: check phone format
    if not _is_valid_phone_number(new_phone):
        return False

    # 4. Update database if user exists
    user_record = database.get(user_id)
    if user_record is None:
        return False

    # Perform the update
    user_record["phone"] = new_phone
    return True


# Example usage (for testing purposes only)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": "123", "new_phone": "+15559876543"},
    }
    result = modify_user_phone(request)
    print("Update successful:", result)
    print("Updated record:", database["123"])