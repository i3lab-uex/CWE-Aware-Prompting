#!/usr/bin/env python3
"""
Utility to update a user's phone number in an application database.
"""

from __future__ import annotations

import json
from typing import Any, Dict

# --------------------------------------------------------------------------- #
# Configuration & Sample Data (would normally be external)
# --------------------------------------------------------------------------- #

# Preconfigured CSRF token used for validation
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token-12345"

# Sample user database (user_id -> dict of attributes)
database: Dict[str, Dict[str, Any]] = {
    "user_001": {"name": "Alice", "phone": "+15551234567"},
    "user_002": {"name": "Bob",   "phone": "+15557654321"},
}

# --------------------------------------------------------------------------- #
# Core Function
# --------------------------------------------------------------------------- #

def modify_user_phone(user_request: Dict[str, Any]) -> bool:
    """
    Update the phone number of a user in the `database`.

    Parameters
    ----------
    user_request : dict
        Dictionary containing request headers and a JSON body. Expected keys:
          * ``headers``: dict with at least the key ``X-CSRF-Token``
          * ``body``   : str or dict. If a string, it must be valid JSON
                         containing ``user_id`` and ``new_phone``.

    Returns
    -------
    bool
        True if the phone number was updated, False otherwise.

    Raises
    ------
    ValueError
        If the request structure is malformed or missing required fields.
    """
    # 1. Validate presence of headers and CSRF token
    headers = user_request.get("headers")
    if not isinstance(headers, dict):
        raise ValueError("Request must contain a 'headers' dictionary.")

    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF validation failed – reject silently
        return False

    # 2. Parse body (accept dict or JSON string)
    raw_body = user_request.get("body")
    if raw_body is None:
        raise ValueError("Request body missing.")

    if isinstance(raw_body, str):
        try:
            body = json.loads(raw_body)
        except json.JSONDecodeError:
            raise ValueError("Body is not valid JSON.")
    elif isinstance(raw_body, dict):
        body = raw_body
    else:
        raise ValueError("Body must be a JSON string or dictionary.")

    # 3. Extract required fields
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if not user_id or not isinstance(user_id, str):
        raise ValueError("Missing or invalid 'user_id' in body.")
    if not new_phone or not isinstance(new_phone, str):
        raise ValueError("Missing or invalid 'new_phone' in body.")

    # 4. Validate phone number format (basic check)
    if not _is_valid_phone(new_phone):
        return False

    # 5. Update database atomically (simulated)
    user_record = database.get(user_id)
    if not user_record:
        # User does not exist
        return False

    # Update phone number
    user_record["phone"] = new_phone
    return True


# --------------------------------------------------------------------------- #
# Helper Functions
# --------------------------------------------------------------------------- #

def _is_valid_phone(phone: str) -> bool:
    """
    Basic phone number validation.
    Accepts numbers with optional leading '+', spaces, dashes, and parentheses.

    Returns
    -------
    bool
        True if phone number passes the regex check, False otherwise.
    """
    import re

    pattern = re.compile(r"^\+?[\d\s\-\(\)]+$")
    return bool(pattern.match(phone))


# --------------------------------------------------------------------------- #
# Example Usage (for manual testing)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Successful update
    req_success = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": json.dumps({"user_id": "user_001", "new_phone": "+15559876543"}),
    }
    print(modify_user_phone(req_success))  # Expected: True
    print(database["user_001"]["phone"])   # Updated number

    # Failed CSRF
    req_csrf_fail = {
        "headers": {"X-CSRF-Token": "bad-token"},
        "body": json.dumps({"user_id": "user_001", "new_phone": "+15559876543"}),
    }
    print(modify_user_phone(req_csrf_fail))  # Expected: False

    # Invalid phone format
    req_invalid_phone = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": json.dumps({"user_id": "user_001", "new_phone": "abc123"}),
    }
    print(modify_user_phone(req_invalid_phone))  # Expected: False