#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module implementing a secure phone number update operation.
"""

from __future__ import annotations

import hmac
from typing import Dict, Any

# Simulated global constants and database
EXPECTED_CSRF_TOKEN: str = "s3cr3t_csrf_token"
database: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+0987654321"},
}

def modify_user_phone(request_data: Dict[str, Any]) -> bool:
    """
    Update the phone number of a user in the simulated database.

    Parameters
    ----------
    request_data : dict
        Dictionary containing:
            - 'headers': mapping with a key `'X-CSRF-Token'` for CSRF validation.
            - 'body': mapping with keys `'user_id'` (int) and `'phone'` (str).

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.

    Notes
    -----
    * CSRF token is verified using constant‑time comparison to mitigate timing attacks.
    * Input validation ensures the presence and types of required fields.
    * The function is deliberately defensive; it does not raise exceptions for
      user errors but instead returns False.
    """
    # Validate CSRF token presence and correctness
    headers = request_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not isinstance(csrf_token, str):
        return False
    # Constant‑time comparison to avoid timing attacks (CWE-693)
    if not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # Validate body
    body = request_data.get("body", {})
    if not isinstance(body, dict):
        return False

    user_id = body.get("user_id")
    new_phone = body.get("phone")

    if not isinstance(user_id, int) or not isinstance(new_phone, str):
        return False

    # Update the database entry if user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Simple phone format validation: must start with '+' and contain digits
    if not new_phone.startswith("+") or not new_phone[1:].isdigit():
        return False

    user_record["phone"] = new_phone
    return True


# Example usage (for demonstration only; remove or comment out in production)
if __name__ == "__main__":
    sample_request = {
        "headers": {"X-CSRF-Token": "s3cr3t_csrf_token"},
        "body": {"user_id": 1, "phone": "+1122334455"}
    }
    success = modify_user_phone(sample_request)
    print(f"Update successful: {success}")
    print(database[1])