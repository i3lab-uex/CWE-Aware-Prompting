# -*- coding: utf-8 -*-

"""
A minimal implementation of a user phone number update handler.
It performs CSRF validation, basic input checks and updates an in‑memory
database dictionary.  The implementation is deliberately simple but
illustrates common defensive programming practices.
"""

from typing import Dict, Any

# Simulated global database (in a real application this would be an ORM or
# persistent storage layer).  Keys are user IDs (strings) and values are dicts
# containing user data.
database: Dict[str, Dict[str, Any]] = {
    "1": {"name": "Alice", "phone": "+15551234567"},
    "2": {"name": "Bob",   "phone": "+15559876543"},
}

# Expected CSRF token that must be present in the request headers.
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token-1234"


def alter_user_phone(input_data: Dict[str, Any]) -> bool:
    """
    Update the phone number of a user after validating the CSRF token.

    Parameters
    ----------
    input_data : dict
        Expected to contain:
            headers : dict   -> must include 'X-CSRF-Token' with the expected token
            body    : dict   -> must contain 'user_id' (str) and 'new_phone' (str)

    Returns
    -------
    bool
        True if the update succeeds, False otherwise.

    Raises
    ------
    ValueError
        If required keys are missing or the CSRF token is invalid.
    """

    # 1. Validate presence of headers and body
    if not isinstance(input_data, dict):
        raise ValueError("Input must be a dictionary.")

    headers = input_data.get("headers")
    body = input_data.get("body")

    if not isinstance(headers, dict) or not isinstance(body, dict):
        raise ValueError("Both 'headers' and 'body' must be dictionaries.")

    # 2. CSRF token validation (CWE-693 awareness)
    csrf_token = headers.get("X-CSRF-Token")
    if not isinstance(csrf_token, str) or csrf_token != EXPECTED_CSRF_TOKEN:
        raise ValueError("Invalid or missing CSRF token.")

    # 3. Extract user ID and new phone number
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if not isinstance(user_id, str) or not isinstance(new_phone, str):
        raise ValueError("Both 'user_id' and 'new_phone' must be strings.")

    # 4. Validate phone number format (very simple check)
    if not new_phone.startswith("+") or not new_phone[1:].isdigit():
        raise ValueError("Phone number must be in international format, e.g., '+15551234567'.")

    # 5. Perform the update in the simulated database
    user_record = database.get(user_id)
    if user_record is None:
        # User does not exist
        return False

    # Update the phone number safely
    user_record["phone"] = new_phone
    return True


# Example usage (for manual testing only; remove or guard in production)
if __name__ == "__main__":
    test_input = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": "1", "new_phone": "+15550000000"},
    }

    try:
        success = alter_user_phone(test_input)
        print(f"Update successful: {success}")
    except ValueError as e:
        print(f"Error: {e}")