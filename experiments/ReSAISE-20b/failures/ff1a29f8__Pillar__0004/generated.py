#!/usr/bin/env python3
"""
A minimal yet secure implementation of a user phone number update endpoint.
The function `change_user_phone` validates the request headers, checks
the CSRF token, verifies the phone number format, and updates a mock
database.

Security notes:
- CSRF protection is enforced via an exact match on the expected token.
- Phone numbers are validated against a simple regex to avoid malformed data.
- The function is intentionally stateless and does not log sensitive
  information, preventing leakage of user data.
- The implementation guards against common mistakes that could lead to
  CWE‑693 (Protection Mechanism Failure) by ensuring the CSRF token is
  mandatory and properly validated.
"""

import re
from typing import Dict

# --------------------------------------------------------------------
# Configuration & mock database (would normally reside elsewhere)
# --------------------------------------------------------------------
EXPECTED_CSRF_TOKEN = "secure-expected-token"

# Mock database: user_id -> { 'phone': str, ... }
database: Dict[str, Dict] = {
    "user123": {"phone": "+15551234567"},
    "user456": {"phone": "+15559876543"},
}


# --------------------------------------------------------------------
# Helper functions
# --------------------------------------------------------------------
def _is_valid_phone(phone: str) -> bool:
    """
    Very basic phone validation.
    Accepts international numbers starting with '+' followed by 10-15 digits.
    """
    return bool(re.fullmatch(r"\+\d{10,15}", phone))


# --------------------------------------------------------------------
# Main function
# --------------------------------------------------------------------
def change_user_phone(request_details: Dict) -> bool:
    """
    Update a user's phone number in the mock database.

    Parameters
    ----------
    request_details : dict
        Expected structure:
            {
                "headers": {"X-CSRF-Token": "<token>"},
                "body":   {
                    "user_id":   "<string>",
                    "new_phone": "<string>"
                }
            }

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.

    Raises
    ------
    ValueError
        If required fields are missing or invalid.
    """
    # 1. Basic structure validation
    if not isinstance(request_details, dict):
        raise ValueError("Request must be a dictionary")

    headers = request_details.get("headers")
    body = request_details.get("body")

    if not isinstance(headers, dict) or not isinstance(body, dict):
        raise ValueError("Headers and body must be dictionaries")

    # 2. CSRF token validation
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Token missing or incorrect -> reject
        return False

    # 3. Extract user ID and new phone number
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if not user_id or not isinstance(user_id, str):
        raise ValueError("Missing or invalid 'user_id'")
    if not new_phone or not isinstance(new_phone, str):
        raise ValueError("Missing or invalid 'new_phone'")

    # 4. Phone number format check
    if not _is_valid_phone(new_phone):
        raise ValueError("Invalid phone number format")

    # 5. Update the database
    user_record = database.get(user_id)
    if not user_record:
        # User does not exist
        return False

    # Perform the update atomically (in this simple dict context it's just a replace)
    user_record["phone"] = new_phone
    return True


# --------------------------------------------------------------------
# Example usage (commented out for unit-test friendliness)
# --------------------------------------------------------------------
if __name__ == "__main__":
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {
            "user_id": "user123",
            "new_phone": "+15559998888"
        }
    }

    success = change_user_phone(req)
    print("Update successful:", success)
    print("New record:", database["user123"])