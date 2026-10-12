#!/usr/bin/env python3
"""
Utility to update a user's phone number in a simple in‑memory database.
The function validates the CSRF token, checks that required fields are
present and well‑formed, and performs a safe update.

CWE-693: Protection Mechanism Failure – this module uses an explicit
CSRF token check and validates input to mitigate common web attacks.
"""

import re
from typing import Dict, Any

# Sample in‑memory user database: {user_id: {"phone": str, ...}}
database: Dict[str, Dict[str, Any]] = {
    "user1": {"phone": "+15551234567"},
    "user2": {"phone": "+15557654321"},
}

# Expected CSRF token (would normally be stored securely)
EXPECTED_CSRF_TOKEN = "s3cr3tCrsfT0k3n"

# Regular expression for a basic international phone number format
PHONE_REGEX = re.compile(r"^\+?[1-9]\d{1,14}$")


def alter_user_phone(service_request: Dict[str, Any]) -> bool:
    """
    Update the phone number of a user.

    Parameters
    ----------
    service_request : dict
        Dictionary containing HTTP headers and body. Expected keys:
            - "headers": {"X-CSRF-Token": str}
            - "body": {"user_id": str, "new_phone": str}

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.

    Notes
    -----
    - Validates CSRF token.
    - Ensures user_id exists in the database.
    - Validates phone number format (basic international E.164).
    - Performs an atomic update in the in-memory dictionary.
    """
    # 1. Validate CSRF token
    headers = service_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body and required fields
    body = service_request.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if not all([user_id, new_phone]):
        return False

    # 3. Validate phone number format
    if not PHONE_REGEX.match(new_phone):
        return False

    # 4. Update the database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Perform the update; in a real system this would involve
    # database transaction handling.
    user_record["phone"] = new_phone
    return True


# Example usage (for testing purposes only)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": "user1", "new_phone": "+15559876543"},
    }
    result = alter_user_phone(request)
    print(f"Update successful: {result}")
    print("Updated database entry:", database["user1"])