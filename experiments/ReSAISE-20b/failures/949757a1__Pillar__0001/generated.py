#!/usr/bin/env python3
"""
Implementation of the change_user_contact function.
"""

import re
from typing import Dict

# --------------------------------------------------------------------
# Global context (normally injected or configured elsewhere)
# --------------------------------------------------------------------

# Sample in‑memory user database.
# Keys are integer user IDs, values are dicts with a 'phone' field.
database: Dict[int, Dict[str, str]] = {
    1: {"phone": "5551234567"},
    2: {"phone": "5559876543"},
}

# Expected CSRF token (would normally be stored securely)
EXPECTED_CSRF_TOKEN = "a1b2c3d4e5f6g7h8i9j0"

# Regular expression for a valid phone number:
# 10 to 15 digits, optionally with spaces or dashes.
PHONE_REGEX = re.compile(r"^[\d\s-]{10,15}$")

# --------------------------------------------------------------------
# Function
# --------------------------------------------------------------------

def change_user_contact(transaction_request: Dict) -> bool:
    """
    Update a user's phone number in the database.

    Parameters
    ----------
    transaction_request : dict
        Dictionary containing 'headers' and 'body'.
        Expected keys:
            - headers: dict with a 'X-CSRF-Token' entry.
            - body: dict containing:
                * user_id : int
                * new_phone : str

    Returns
    -------
    bool
        True if the phone number was updated successfully,
        False otherwise.
    """
    # 1. Validate request structure
    if not isinstance(transaction_request, dict):
        return False

    headers = transaction_request.get("headers", {})
    body = transaction_request.get("body", {})

    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # 2. CSRF protection
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Potential CSRF attack detected
        return False

    # 3. Extract user ID and new phone number
    try:
        user_id = int(body["user_id"])
        new_phone = str(body["new_phone"]).strip()
    except (KeyError, ValueError, TypeError):
        return False

    # 4. Validate phone number format
    if not PHONE_REGEX.match(new_phone):
        return False

    # 5. Update the database
    user_record = database.get(user_id)
    if not user_record:
        # User does not exist
        return False

    # Perform the update (simple assignment)
    user_record["phone"] = new_phone
    return True

# --------------------------------------------------------------------
# Example usage (for testing purposes only)
# --------------------------------------------------------------------
if __name__ == "__main__":
    # Successful update
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_phone": "555-000-1111"},
    }
    print(change_user_contact(req))  # Expected: True
    print(database[1]["phone"])     # Expected: "555-000-1111"

    # Failure due to wrong CSRF token
    bad_req = {
        "headers": {"X-CSRF-Token": "badtoken"},
        "body": {"user_id": 1, "new_phone": "555-000-1111"},
    }
    print(change_user_contact(bad_req))  # Expected: False