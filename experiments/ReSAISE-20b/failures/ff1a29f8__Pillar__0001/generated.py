import re
import hmac
from typing import Dict

# Mock database and constants for the example
database: Dict[int, Dict[str, str]] = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"},
}

EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_12345"

# Regular expression for validating international phone numbers (E.164 format)
PHONE_REGEX = re.compile(r"^\+?[1-9]\d{1,14}$")


def change_user_phone(request_details: Dict) -> bool:
    """
    Update a user's phone number after validating CSRF token and input data.

    Args:
        request_details (dict): Contains 'headers' with CSRF token and
                                'body' with 'user_id' (int) and 'new_phone' (str).

    Returns:
        bool: True if the update succeeded, False otherwise.

    Raises:
        None (function handles all errors internally and returns False).
    """
    try:
        # Extract headers and body
        headers = request_details.get("headers", {})
        body = request_details.get("body", {})

        # CSRF token validation using constant‑time comparison
        csrf_token = headers.get("X-CSRF-Token")
        if not csrf_token or not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
            return False

        # Validate user_id
        user_id = body.get("user_id")
        if not isinstance(user_id, int):
            return False

        # Validate new phone number format
        new_phone = body.get("new_phone")
        if not isinstance(new_phone, str) or not PHONE_REGEX.match(new_phone):
            return False

        # Check if user exists in the database
        user_record = database.get(user_id)
        if not user_record:
            return False

        # Update phone number
        user_record["phone"] = new_phone
        return True

    except Exception:
        # Any unexpected error should not expose details; just fail safely
        return False


# Example usage (for testing purposes only)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": "secure_csrf_token_12345"},
        "body": {"user_id": 1, "new_phone": "+15551234567"},
    }
    print(change_user_phone(request))  # Expected: True
    print(database[1]["phone"])        # Expected: "+15551234567"