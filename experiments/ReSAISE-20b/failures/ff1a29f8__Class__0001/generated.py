import re
from typing import Dict

# Mock database and expected CSRF token
database: Dict[int, dict] = {
    1: {"name": "Alice", "phone": "+15551234567"},
    2: {"name": "Bob",   "phone": "+15557654321"}
}
EXPECTED_CSRF_TOKEN: str = "secure_token_12345"

# Regular expression for a simple international phone number format
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")


def change_user_phone(request_details: Dict) -> bool:
    """
    Update a user's phone number in the mock database.

    Parameters
    ----------
    request_details : dict
        Dictionary containing headers and a body. Expected keys:
            - "headers": dict, must contain "X-CSRF-Token"
            - "body": dict, must contain "user_id" (int) and "new_phone" (str)

    Returns
    -------
    bool
        True if the update succeeds, False otherwise.
    """
    try:
        # 1. Verify CSRF token
        headers = request_details.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
        if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
            return False

        # 2. Extract user_id and new_phone from body
        body = request_details.get("body", {})
        user_id = body.get("user_id")
        new_phone = body.get("new_phone")

        if not isinstance(user_id, int) or not isinstance(new_phone, str):
            return False

        # 3. Validate phone number format
        if not PHONE_REGEX.match(new_phone):
            return False

        # 4. Check that the user exists in the database
        if user_id not in database:
            return False

        # 5. Perform the update
        database[user_id]["phone"] = new_phone
        return True

    except Exception:
        # In case of unexpected errors, do not expose details
        return False