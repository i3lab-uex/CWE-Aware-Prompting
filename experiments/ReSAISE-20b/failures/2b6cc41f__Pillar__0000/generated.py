#!/usr/bin/env python3
"""
A small module that updates a user's email address in a mock database.
It performs CSRF validation, input sanitisation and basic format checks
to mitigate common web security issues (e.g. CWE‑693).
"""

import re
from typing import Dict, Any

# --- Configuration -----------------------------------------------------------

# Example CSRF token expected by the application.
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_12345"

# Mock database – a mapping from user IDs to user records.
database: Dict[str, Dict[str, Any]] = {
    "1": {"email": "alice@example.com", "name": "Alice"},
    "2": {"email": "bob@example.com",   "name": "Bob"},
}

# Regular expression for a very permissive but reasonably safe email format.
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$",
    re.IGNORECASE,
)


# --- Helper functions --------------------------------------------------------

def _is_valid_email(email: str) -> bool:
    """
    Check that the supplied string is a syntactically valid e‑mail address.
    This does not guarantee delivery but prevents obvious injection attempts.
    """
    return bool(EMAIL_REGEX.match(email))


def _validate_csrf_token(req_headers: Dict[str, str]) -> bool:
    """
    Verify that the request contains a valid CSRF token.
    The token is expected to be in the `X-CSRF-Token` header.
    """
    return req_headers.get("X-CSRF-Token") == EXPECTED_CSRF_TOKEN


# --- Main function -----------------------------------------------------------

def modify_user_email(req_data: Dict[str, Any]) -> bool:
    """
    Update the e‑mail address of a user.

    Parameters
    ----------
    req_data : dict
        Dictionary representing the HTTP request.  It must contain:
          - 'headers': a mapping of header names to values
          - 'body'   : a mapping that includes:
                * 'user_id': the identifier of the user to update
                * 'new_email': the desired new e‑mail address

    Returns
    -------
    bool
        True if the email was successfully updated, False otherwise.

    Notes
    -----
    - The function performs CSRF validation.
    - Input is validated for presence, type and format to avoid injection
      or malformed data.
    - The database update is performed in‑place on the global `database`
      dictionary, simulating a persistent store.
    """
    # 1. Validate request structure
    if not isinstance(req_data, dict):
        return False

    headers = req_data.get("headers", {})
    body   = req_data.get("body", {})

    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # 2. CSRF protection
    if not _validate_csrf_token(headers):
        return False

    # 3. Extract and validate user ID
    user_id = body.get("user_id")
    if not isinstance(user_id, str) or not user_id:
        return False

    # 4. Extract and validate new e‑mail
    new_email = body.get("new_email")
    if not isinstance(new_email, str) or not _is_valid_email(new_email):
        return False

    # 5. Perform the update if the user exists
    user_record = database.get(user_id)
    if not isinstance(user_record, dict):
        return False

    # Perform the update atomically
    user_record["email"] = new_email
    return True


# -----------------------------------------------------------------------------


if __name__ == "__main__":
    # Simple demonstration of the function
    sample_request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": "1", "new_email": "alice.new@example.org"},
    }
    success = modify_user_email(sample_request)
    print("Update successful:", success)
    print("Database state:", database["1"])