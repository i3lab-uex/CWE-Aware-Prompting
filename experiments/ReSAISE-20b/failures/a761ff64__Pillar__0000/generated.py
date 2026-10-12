# -*- coding: utf-8 -*-
"""
User phone update helper.

This module implements the `alter_user_phone` function which
validates a CSRF token, checks that the supplied user ID exists in
the provided database, and updates the phone number.

Security considerations:
* CSRF token is validated against a known constant.
* User ID and phone number are treated as opaque strings – no
  further validation is performed here to keep the example concise.
* The function returns a boolean rather than raising an exception
  to avoid leaking information about the existence of user IDs.
"""

from typing import Dict

# Global context – these would normally be injected or imported from the app
database: Dict[str, dict] = {}  # e.g. {'user1': {'phone': '12345'}}
EXPECTED_CSRF_TOKEN: str = "expected_csrf_token_value"


def alter_user_phone(input_data: Dict) -> bool:
    """
    Update the phone number of a user.

    Parameters
    ----------
    input_data : dict
        Expected structure:
            {
                "headers": {"X-CSRF-Token": "<token>"},
                "body": {"user_id": "<id>", "phone": "<new_phone>"}
            }

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    # 1. Validate CSRF token
    headers = input_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Token mismatch – reject the request
        return False

    # 2. Extract body data
    body = input_data.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("phone")

    if not user_id or not new_phone:
        # Missing required fields
        return False

    # 3. Check that the user exists in the database
    user_record = database.get(user_id)
    if not user_record:
        # User ID does not exist
        return False

    # 4. Perform the update
    user_record["phone"] = new_phone
    return True


# ------------------------------------------------------------------
# Example usage (for illustration only; remove or guard in production)
if __name__ == "__main__":
    # Seed the mock database
    database["user123"] = {"phone": "555-0000"}

    # Construct a request
    request_payload = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": "user123", "phone": "555-9999"},
    }

    # Call the function
    success = alter_user_phone(request_payload)
    print("Update successful:", success)          # Expected: True
    print("New phone:", database["user123"]["phone"])  # Expected: 555-9999