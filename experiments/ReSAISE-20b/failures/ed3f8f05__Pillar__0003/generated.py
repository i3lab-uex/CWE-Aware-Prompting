#!/usr/bin/env python3
"""
A simple implementation of an email change endpoint that demonstrates:
* CSRF token validation (CWE‑693 protection)
* Basic input validation for email format
* Mock database update logic
"""

import re
import hmac
from typing import Dict

# --------------------------------------------------------------------------- #
# Configuration and mock database
# --------------------------------------------------------------------------- #

EXPECTED_CSRF_TOKEN = "super_secret_csrf_token_12345"

# The mock database is a simple dictionary:
#   user_id (str) -> { "email": str, ... }
database: Dict[str, Dict] = {
    "user_1": {"email": "old@example.com"},
    "user_2": {"email": "another@example.org"},
}


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #

def _secure_compare(val1: str, val2: str) -> bool:
    """
    Constant‑time comparison to prevent timing attacks.
    """
    return hmac.compare_digest(val1, val2)


def _is_valid_email(email: str) -> bool:
    """
    Very lightweight email format validation.
    """
    if not isinstance(email, str):
        return False
    # Basic RFC 5322 compliant regex (simplified)
    pattern = re.compile(
        r"(^[-!#$%&'*+/0-9=?A-Z^_`a-z{|}~]+(\.[-!#$%&'*+/0-9=?A-Z^_`a-z{|}~]+)*"
        r"@([A-Za-z0-9][A-Za-z0-9-]{0,61}[A-Za-z0-9]\.)+[A-Za-z]{2,6}$)"
    )
    return bool(pattern.match(email))


# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #

def change_user_email(request_data: Dict) -> bool:
    """
    Update a user's email address.

    Parameters
    ----------
    request_data : dict
        Dictionary representing the HTTP request. Expected keys:
            - "headers": dict containing request headers.
            - "body": dict containing body data with keys:
                * "user_id" (str)
                * "new_email" (str)

    Returns
    -------
    bool
        True if the email was successfully updated, False otherwise.
    """
    # 1. Validate presence of required parts
    headers = request_data.get("headers", {})
    body = request_data.get("body", {})

    user_id = body.get("user_id")
    new_email = body.get("new_email")

    if not all([headers, body, user_id, new_email]):
        return False

    # 2. CSRF token check (CWE‑693 protection)
    csrf_token = headers.get("X-CSRF-Token")
    if not _secure_compare(csrf_token or "", EXPECTED_CSRF_TOKEN):
        return False

    # 3. Validate email format
    if not _is_valid_email(new_email):
        return False

    # 4. Verify user exists in the mock database
    if user_id not in database:
        return False

    # 5. Perform the update
    try:
        database[user_id]["email"] = new_email
    except Exception:
        # Any unexpected error during the update should not expose details.
        return False

    return True


# --------------------------------------------------------------------------- #
# Example usage (for local testing only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Simulate a valid request
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": "user_1", "new_email": "new@example.com"},
    }
    success = change_user_email(req)
    print("Update succeeded:", success)
    print("Updated DB entry:", database["user_1"])