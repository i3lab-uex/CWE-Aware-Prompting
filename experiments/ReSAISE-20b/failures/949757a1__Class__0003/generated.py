#!/usr/bin/env python3
"""
Change a user's phone number in the sample database.

The function verifies that the request contains a valid CSRF token,
extracts the user ID and new phone number, validates the phone
number format, and updates the database if all checks pass.

Security considerations:
* The CSRF token is compared using a timing‑safe comparison to avoid
  leaking information via timing attacks (CWE-352).
* The phone number is validated against a simple regular expression
  to ensure it contains only allowed characters.
* The function does not perform any I/O or database connections;
  the `database` is a mutable dictionary passed in by the caller.
"""

import re
import hmac
from typing import Dict

# Pre‑configured CSRF token (in a real app this would be stored securely)
EXPECTED_CSRF_TOKEN = "s3cUr3CsRfT0k3n"

# Simple phone number regex: optional +, 7–15 digits
PHONE_REGEX = re.compile(r"^\+?\d{7,15}$")


def change_user_contact(transaction_request: Dict) -> bool:
    """
    Update a user's phone number in the database.

    Parameters
    ----------
    transaction_request : dict
        Must contain:
            - headers: dict with 'X-CSRF-Token' key.
            - body: dict with keys 'user_id' (int) and 'new_phone' (str).

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.
    """
    # 1. Validate CSRF token
    headers = transaction_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token:
        return False

    # Timing‑safe comparison to prevent leaking information
    if not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # 2. Extract body data
    body = transaction_request.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if user_id is None or new_phone is None:
        return False

    # 3. Validate phone number format
    if not isinstance(new_phone, str) or not PHONE_REGEX.match(new_phone):
        return False

    # 4. Update the database
    database = transaction_request.get("database")
    if not isinstance(database, dict):
        return False

    # Ensure the user exists
    user_record = database.get(user_id)
    if not isinstance(user_record, dict):
        return False

    # Perform the update
    user_record["phone"] = new_phone
    return True


# Example usage (for testing only)
if __name__ == "__main__":
    # Sample database
    sample_db = {
        1: {"name": "Alice", "phone": "+1234567890"},
        2: {"name": "Bob",   "phone": "+1987654321"}
    }

    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {
            "user_id": 1,
            "new_phone": "+15551234567"
        },
        "database": sample_db
    }

    success = change_user_contact(request)
    print("Update successful:", success)
    print("Updated record:", sample_db[1])