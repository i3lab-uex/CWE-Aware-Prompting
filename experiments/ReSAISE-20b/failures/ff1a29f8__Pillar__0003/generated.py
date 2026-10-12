#!/usr/bin/env python3
"""
Implementation of a secure user phone number update routine.
"""

import re
import hmac
from typing import Dict

# Mock database: user_id -> { 'phone': str, ... }
database: Dict[str, Dict] = {}

# Expected CSRF token for the application
EXPECTED_CSRF_TOKEN: str = "s3cureT0k3n123"

# Regular expression for a simple E.164 phone number validation
PHONE_REGEX = re.compile(r"^\+?[1-9]\d{1,14}$")


def _validate_csrf_token(token: str) -> bool:
    """
    Securely compare the provided CSRF token against the expected one.
    Uses constant‑time comparison to mitigate timing attacks.

    Args:
        token: The CSRF token from the request header.

    Returns:
        True if tokens match, False otherwise.
    """
    return hmac.compare_digest(token.encode(), EXPECTED_CSRF_TOKEN.encode())


def _validate_phone_number(phone: str) -> bool:
    """
    Validate the phone number against a simple E.164 format.

    Args:
        phone: The new phone number string.

    Returns:
        True if the format is acceptable, False otherwise.
    """
    return bool(PHONE_REGEX.match(phone))


def change_user_phone(request_details: Dict) -> bool:
    """
    Update a user's phone number in the mock database after performing
    CSRF protection, input validation and existence checks.

    Args:
        request_details: Dictionary containing the request headers
                         and body with keys 'user_id' and 'new_phone'.

    Returns:
        True if the phone number was successfully updated, False otherwise.
    """
    try:
        # Extract headers and body
        headers = request_details.get("headers", {})
        body = request_details.get("body", {})

        # CSRF protection
        csrf_token = headers.get("X-CSRF-Token")
        if not csrf_token or not _validate_csrf_token(csrf_token):
            return False

        # Required fields
        user_id = body.get("user_id")
        new_phone = body.get("new_phone")

        if not user_id or not new_phone:
            return False

        # Input validation
        if not _validate_phone_number(new_phone):
            return False

        # Check that the user exists
        if user_id not in database:
            return False

        # Perform the update
        database[user_id]["phone"] = new_phone
        return True

    except Exception:
        # Log exception in real application; here we simply fail safely
        return False


# ------------------------------------------------------------------
# Example usage (for demonstration purposes only)
if __name__ == "__main__":
    # Populate mock database
    database["user123"] = {"phone": "+15551234567", "name": "Alice"}

    # Create a request
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": "user123", "new_phone": "+15557654321"}
    }

    result = change_user_phone(req)
    print("Update successful:", result)
    print("Updated record:", database["user123"])