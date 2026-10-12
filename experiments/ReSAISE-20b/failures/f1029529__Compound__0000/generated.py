#!/usr/bin/env python3
"""
A simple, secure implementation of a phone‑number update endpoint.

The function:
* verifies the CSRF token to mitigate CWE‑352.
* validates input types and basic phone format.
* updates a mock database dictionary.
"""

import re
from typing import Dict, Any

# Mock database: user_id -> dict with 'phone' field
database: Dict[str, Dict[str, Any]] = {
    "user1": {"phone": "+15551234567"},
    "user2": {"phone": "+441234567890"},
}

# Expected CSRF token (in a real app this would be per‑session)
EXPECTED_CSRF_TOKEN = "s3cr3t-csrf-token"

# Regular expression for a very permissive international phone number
PHONE_REGEX = re.compile(r"^\+?[0-9]{7,15}$")


def _validate_phone(phone: str) -> bool:
    """Return True if the phone number matches the expected pattern."""
    return bool(PHONE_REGEX.match(phone))


def modify_user_phone(client_request: Dict[str, Any]) -> bool:
    """
    Update a user's phone number in the mock database.

    Parameters
    ----------
    client_request : dict
        Dictionary containing:
            headers: {'X-CSRF-Token': str}
            body:   {'user_id': str, 'new_phone': str}

    Returns
    -------
    bool
        True if the update succeeds, False otherwise.
    """
    try:
        # 1. CSRF protection
        headers = client_request.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            return False

        # 2. Extract body data
        body = client_request.get("body", {})
        user_id = str(body.get("user_id", "")).strip()
        new_phone = str(body.get("new_phone", "")).strip()

        # 3. Basic validation
        if not user_id or not new_phone:
            return False
        if not _validate_phone(new_phone):
            return False

        # 4. Update database
        user_record = database.get(user_id)
        if not user_record:
            return False

        # Update the phone number atomically
        database[user_id]["phone"] = new_phone
        return True

    except Exception:
        # In a real application you would log the exception.
        return False


# Example usage (for local testing only)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": "user1", "new_phone": "+15557654321"},
    }
    success = modify_user_phone(request)
    print("Update succeeded:", success)
    print("New DB state:", database["user1"])