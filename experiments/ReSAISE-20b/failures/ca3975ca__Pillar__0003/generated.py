#!/usr/bin/env python3
"""
User phone number modification handler.

This module defines `modify_user_phone`, which validates a CSRF token,
extracts the user ID and new phone number from the request payload,
and updates a simulated in-memory database.

Security considerations:
- CSRF token is strictly compared to EXPECTED_CSRF_TOKEN.
- Input values are type‑checked and sanitized to prevent injection
  or accidental type errors.
- The function does not raise on failure; it returns a boolean,
  preventing stack traces from leaking sensitive information
  (mitigating CWE‑693).
"""

from typing import Dict, Any

# Simulated in-memory user database.
# Each user entry is a dict containing at least the key 'phone'.
database: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"},
}

# Pre‑defined CSRF token that must be present in the request.
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"


def modify_user_phone(request_data: Dict[str, Any]) -> bool:
    """
    Update the phone number for a specific user.

    Parameters
    ----------
    request_data : dict
        Dictionary containing:
            - headers: dict with key 'X-CSRF-Token'
            - body:   dict with keys 'user_id' (int) and
                      'new_phone' (str)

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    # --- CSRF protection ----------------------------------------------------
    headers = request_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")

    if csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF token missing or invalid.
        return False

    # --- Extract body data --------------------------------------------------
    body = request_data.get("body", {})
    user_id_raw = body.get("user_id")
    new_phone_raw = body.get("new_phone")

    # Validate presence
    if user_id_raw is None or new_phone_raw is None:
        return False

    # Validate types
    try:
        user_id = int(user_id_raw)
    except (TypeError, ValueError):
        return False

    if not isinstance(new_phone_raw, str) or not new_phone_raw.strip():
        return False

    new_phone = new_phone_raw.strip()

    # --- Update the database ------------------------------------------------
    user_record = database.get(user_id)
    if user_record is None:
        # User does not exist
        return False

    # Basic phone number format check (very loose)
    if not all(c.isdigit() or c in "+- " for c in new_phone):
        return False

    # Perform the update
    user_record["phone"] = new_phone
    return True


# Example usage (for testing purposes only)
if __name__ == "__main__":
    test_request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_phone": "+1112223333"},
    }
    success = modify_user_phone(test_request)
    print(f"Update successful: {success}")
    print(f"Updated record: {database[1]}")