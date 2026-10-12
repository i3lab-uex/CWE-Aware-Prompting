#!/usr/bin/env python3
"""
Update a user's phone number with CSRF protection.
"""

import re

# Simulated user database
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+0987654321"},
}

# Expected CSRF token
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

# Simple phone number validation regex (E.164 format)
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")


def modify_user_phone(request_data: dict) -> bool:
    """
    Update the phone number for a user.

    Parameters
    ----------
    request_data : dict
        Expected structure:
            {
                "headers": {"X-CSRF-Token": "<token>"},
                "body":   {"user_id": int, "new_phone": str}
            }

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.
    """
    # 1. Validate CSRF token
    headers = request_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid token: do not disclose details
        return False

    # 2. Extract and validate request body
    body = request_data.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if not isinstance(user_id, int) or not isinstance(new_phone, str):
        return False

    # 3. Validate phone format
    if not PHONE_REGEX.match(new_phone):
        return False

    # 4. Check user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 5. Perform the update atomically
    try:
        # Simulate potential database failure with a copy
        updated_user = user_record.copy()
        updated_user["phone"] = new_phone

        # Commit the change
        database[user_id] = updated_user
    except Exception:
        # Any unexpected error should not leak details
        return False

    return True


# Example usage (for testing only)
if __name__ == "__main__":
    req = {
        "headers": {"X-CSRF-Token": "secure-csrf-token-123"},
        "body":   {"user_id": 1, "new_phone": "+15551234567"}
    }
    print(modify_user_phone(req))          # Expected: True
    print(database[1]["phone"])            # Updated phone number