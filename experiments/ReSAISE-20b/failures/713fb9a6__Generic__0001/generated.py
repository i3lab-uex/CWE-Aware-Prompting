#!/usr/bin/env python3
"""
Utility module for updating a user's phone number in a simulated web application.

The main entry point is :func:`change_user_phone` which validates the CSRF token,
ensures the user exists, and updates their phone number in a global ``database``
dictionary.

The module intentionally keeps external dependencies minimal and focuses on
security best practices such as token validation, type checking, and safe data
access.
"""

from __future__ import annotations

import re
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Configuration & Simulated Database
# --------------------------------------------------------------------------- #

# Pre‑defined CSRF token that must match the request header.
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_12345"

# A simple in‑memory user database.
# Keys are integer user IDs, values are dictionaries containing user data.
database: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "phone": "+15551234567"},
    2: {"name": "Bob",   "phone": "+15559876543"},
    # ... more users
}

# --------------------------------------------------------------------------- #
# Helper Functions
# --------------------------------------------------------------------------- #

def _is_valid_phone_number(phone: str) -> bool:
    """
    Basic validation for international phone numbers.
    Accepts strings that start with '+' followed by 10 to 15 digits.
    """
    return bool(re.fullmatch(r"\+\d{10,15}", phone))

# --------------------------------------------------------------------------- #
# Main Function
# --------------------------------------------------------------------------- #

def change_user_phone(payload: Dict[str, Any]) -> bool:
    """
    Update the phone number of a user.

    Parameters
    ----------
    payload : dict
        Request dictionary containing:
            * ``headers``: mapping that must include the CSRF token under key
              ``"X-CSRF-Token"``.
            * ``body``: mapping that must include:
                - ``user_id`` (int): the ID of the user to update.
                - ``new_phone`` (str): the new phone number.

    Returns
    -------
    bool
        ``True`` if the phone was updated successfully,
        ``False`` otherwise (e.g., token mismatch, user not found, or
        invalid phone format).

    Notes
    -----
    * The function does **not** raise exceptions on failure; it simply returns
      ``False`` to allow callers to handle the outcome gracefully.
    * The phone number is validated against a simple regex; in production
      environments you would use a dedicated library such as ``phonenumbers``.
    """
    # Validate payload structure
    if not isinstance(payload, dict):
        return False

    headers = payload.get("headers")
    body   = payload.get("body")

    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # 1. CSRF Token validation
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract and validate user ID
    user_id = body.get("user_id")
    if not isinstance(user_id, int):
        return False

    # 3. Validate new phone number format
    new_phone = body.get("new_phone")
    if not isinstance(new_phone, str) or not _is_valid_phone_number(new_phone):
        return False

    # 4. Ensure user exists
    user_record = database.get(user_id)
    if not isinstance(user_record, dict):
        return False

    # 5. Perform the update
    user_record["phone"] = new_phone
    return True

# --------------------------------------------------------------------------- #
# Example Usage (for manual testing)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    test_payload = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body":    {"user_id": 1, "new_phone": "+15551230000"},
    }

    success = change_user_phone(test_payload)
    print("Update succeeded:", success)
    print("Updated record:", database[1])