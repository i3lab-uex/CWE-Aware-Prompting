#!/usr/bin/env python3
"""
Utility for updating a user's email address in a mock web application.
"""

import re
from typing import Dict, Any

# ----------------------------------------------------------------------
# Configuration & Mock Database
# ----------------------------------------------------------------------
EXPECTED_CSRF_TOKEN = "secure_csrf_token_12345"

# Mock database: user_id -> dict containing user attributes
database: Dict[str, Dict[str, Any]] = {
    "user_1": {"email": "alice@example.com"},
    "user_2": {"email": "bob@example.org"},
}

# ----------------------------------------------------------------------
# Helper Functions
# ----------------------------------------------------------------------


def _is_valid_email(email: str) -> bool:
    """
    Very simple regex-based email validation.
    Does not guarantee deliverability but catches obvious format errors.
    """
    pattern = re.compile(
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    )
    return bool(pattern.match(email))


def _extract_csrf_token(headers: Dict[str, str]) -> str | None:
    """
    Retrieve CSRF token from request headers.
    Accepts 'X-CSRF-Token' or 'csrf-token'.
    """
    return headers.get("X-CSRF-Token") or headers.get("csrf-token")


# ----------------------------------------------------------------------
# Main Function
# ----------------------------------------------------------------------


def edit_user_email(req_payload: Dict[str, Any]) -> bool:
    """
    Update a user's email address.

    Parameters
    ----------
    req_payload : dict
        Dictionary representing an HTTP request. Expected keys:
            - headers: dict of request headers.
            - body:   dict containing 'user_id' and 'new_email'.

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    try:
        # 1. CSRF protection
        headers = req_payload.get("headers", {})
        csrf_token = _extract_csrf_token(headers)
        if csrf_token != EXPECTED_CSRF_TOKEN:
            # CSRF token missing or incorrect
            return False

        # 2. Extract user data from body
        body = req_payload.get("body", {})
        user_id: str | None = body.get("user_id")
        new_email: str | None = body.get("new_email")

        if not user_id or not new_email:
            # Missing required fields
            return False

        # 3. Validate email format
        if not _is_valid_email(new_email):
            return False

        # 4. Ensure user exists
        user_record = database.get(user_id)
        if not user_record:
            return False

        # 5. Update email atomically
        # In a real system, this would be a database transaction.
        user_record["email"] = new_email
        return True

    except Exception:
        # Log exception in real application; here we simply fail gracefully.
        return False