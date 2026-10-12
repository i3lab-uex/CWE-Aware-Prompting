#!/usr/bin/env python3
"""
Utility to modify a user's phone number in a simulated web application.
"""

from __future__ import annotations

import re
from typing import Dict, Any

# Simulated database: mapping user_id -> dict of user attributes
database: Dict[str, Dict[str, Any]] = {}

# Predefined CSRF token that must be matched
EXPECTED_CSRF_TOKEN: str = "SECRET-CsRf-ToKeN-123456"

# Regular expression to validate international phone numbers (simplified)
PHONE_REGEX = re.compile(r"^\+?\d{7,15}$")


def modify_user_phone(request_data: Dict[str, Any]) -> bool:
    """
    Update the phone number of a user in the simulated database.

    Parameters
    ----------
    request_data : dict
        Dictionary expected to contain:
            - headers: dict with key 'X-CSRF-Token'
            - body:   dict with keys 'user_id' and 'new_phone'

    Returns
    -------
    bool
        ``True`` if the phone number was updated successfully,
        ``False`` otherwise.

    Raises
    ------
    ValueError
        If required fields are missing or the CSRF token is invalid.
    """

    # ---- 1. Validate request structure ------------------------------------
    try:
        headers = request_data["headers"]
        body = request_data["body"]
    except KeyError as exc:
        raise ValueError(f"Missing top-level key in request_data: {exc}") from None

    # ---- 2. CSRF token check ---------------------------------------------
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        # Do NOT reveal whether the token was missing or wrong
        return False

    # ---- 3. Extract user id and new phone number -------------------------
    try:
        user_id = body["user_id"]
        new_phone = body["new_phone"]
    except KeyError as exc:
        raise ValueError(f"Missing key in request body: {exc}") from None

    if not isinstance(user_id, str) or not user_id:
        return False
    if not isinstance(new_phone, str):
        return False

    # ---- 4. Validate phone number format ---------------------------------
    if not PHONE_REGEX.match(new_phone):
        return False

    # ---- 5. Update database -----------------------------------------------
    user_record = database.get(user_id)
    if user_record is None:
        return False

    # Optional: store previous phone for audit
    old_phone = user_record.get("phone")
    user_record["phone"] = new_phone

    # In a real system we might log the change here
    _log_phone_change(user_id, old_phone, new_phone)

    return True


# --------------------------------------------------------------------------- #
def _log_phone_change(user_id: str, old_phone: str | None, new_phone: str) -> None:
    """
    Simple audit log for phone number changes.
    In a real application this would write to a persistent log or monitoring system.
    """
    import datetime

    timestamp = datetime.datetime.utcnow().isoformat()
    print(
        f"[{timestamp}] User {user_id} phone changed from "
        f"{old_phone or 'N/A'} to {new_phone}"
    )


# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Example usage and basic test
    database.update(
        {
            "user123": {"name": "Alice", "phone": "+15551234567"},
        }
    )

    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": "user123", "new_phone": "+15559876543"},
    }

    success = modify_user_phone(request)
    print("Update successful:", success)  # Expected: True