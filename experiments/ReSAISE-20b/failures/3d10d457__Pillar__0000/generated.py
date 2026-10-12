import re
from typing import Dict

# Mock database and expected CSRF token for demonstration purposes.
database: Dict[int, Dict[str, str]] = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+0987654321"},
}
EXPECTED_CSRF_TOKEN: str = "s3cureT0k3n"

# Regular expression for a simple international phone number validation.
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")


def alter_user_phone(incoming_request: Dict) -> bool:
    """
    Update a user's phone number in the mock database after verifying CSRF token
    and validating input data.

    Args:
        incoming_request (dict): A dictionary representing the request.
            Expected keys:
                - "headers": dict containing HTTP headers.
                - "body": dict containing "user_id" (int) and "phone" (str).

    Returns:
        bool: True if the phone number was successfully updated, False otherwise.
    """
    try:
        # 1. CSRF token verification
        headers = incoming_request.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            return False

        # 2. Extract and validate request body
        body = incoming_request.get("body", {})
        user_id = body.get("user_id")
        new_phone = body.get("phone")

        if not isinstance(user_id, int) or not isinstance(new_phone, str):
            return False

        # 3. Phone number format validation
        if not PHONE_REGEX.match(new_phone):
            return False

        # 4. Ensure user exists in the database
        if user_id not in database:
            return False

        # 5. Perform the update
        database[user_id]["phone"] = new_phone
        return True

    except Exception:
        # In production, log the exception. Here we simply fail silently.
        return False