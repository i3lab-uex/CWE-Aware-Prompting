import re
from typing import Dict

# Mock database: user_id -> user record dict (contains 'phone' key)
database: Dict[str, Dict] = {
    "user123": {"name": "Alice", "phone": "+15551234567"},
    "user456": {"name": "Bob",   "phone": "+15557654321"},
}

# Expected CSRF token for the request
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token-123"

# Regular expression for a simple E.164 phone number validation
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")


def change_user_phone(request_details: Dict) -> bool:
    """
    Update a user's phone number in the mock database.

    Parameters
    ----------
    request_details : dict
        Expected to contain:
            - headers: dict with a 'X-CSRF-Token' key
            - body: dict with keys:
                * user_id (str)
                * new_phone (str)

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.

    Raises
    ------
    None
    """
    try:
        # 1. CSRF protection: ensure token matches expected value
        headers = request_details.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            return False

        # 2. Extract body data
        body = request_details.get("body", {})
        user_id = body.get("user_id")
        new_phone = body.get("new_phone")

        if not user_id or not new_phone:
            return False

        # 3. Validate phone number format
        if not PHONE_REGEX.match(new_phone):
            return False

        # 4. Check that user exists in database
        user_record = database.get(user_id)
        if not user_record:
            return False

        # 5. Update phone number
        user_record["phone"] = new_phone
        return True

    except Exception:
        # Any unexpected error leads to a failure response
        return False


# Example usage (for testing purposes only)
if __name__ == "__main__":
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": "user123", "new_phone": "+15559876543"},
    }
    print(change_user_phone(req))  # Should output: True
    print(database["user123"]["phone"])  # Updated phone number