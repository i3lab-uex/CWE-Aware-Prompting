#!/usr/bin/env python3
"""
Utility for updating a user's phone number in a mock web application database.
"""

import re
from typing import Dict, Any

# Expected CSRF token for request validation
EXPECTED_CSRF_TOKEN = "secure_csrf_token_12345"

# Mock database: user_id -> dict of user attributes
database: Dict[str, Dict[str, Any]] = {
    "user1": {"name": "Alice", "phone": "+1234567890"},
    "user2": {"name": "Bob",   "phone": "+1987654321"},
}


def _is_valid_phone_number(phone: str) -> bool:
    """
    Validate phone number format.
    Accepts international numbers with optional '+' and 10-15 digits.
    """
    return bool(re.fullmatch(r"\+?\d{10,15}", phone))


def change_user_phone(request_details: Dict[str, Any]) -> bool:
    """
    Update a user's phone number in the mock database.

    Parameters
    ----------
    request_details : dict
        Dictionary representing the HTTP request. Expected keys:
            - 'headers': dict containing request headers.
              Must include 'X-CSRF-Token'.
            - 'body': dict containing:
                * 'user_id' : str, identifier of the user.
                * 'new_phone': str, new phone number.

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    # 1. Validate presence of headers and body
    headers = request_details.get("headers", {})
    body = request_details.get("body", {})

    # 2. CSRF token check
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 3. Extract user_id and new_phone
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if not user_id or not new_phone:
        return False

    # 4. Validate phone number format
    if not _is_valid_phone_number(new_phone):
        return False

    # 5. Update the database if user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 6. Perform the update
    user_record["phone"] = new_phone
    return True


# Example usage (for manual testing only; remove or comment out in production)
if __name__ == "__main__":
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": "user1", "new_phone": "+1122334455"},
    }
    success = change_user_phone(req)
    print("Update successful:", success)
    print("Updated database entry:", database.get("user1"))