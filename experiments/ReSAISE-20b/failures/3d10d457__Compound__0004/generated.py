import re
import json

# Mock database and CSRF token for demonstration purposes
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+0987654321"}
}
EXPECTED_CSRF_TOKEN = "secure_token_123"

# Regular expression for basic E.164 phone number validation
PHONE_REGEX = re.compile(r"^\+?[1-9]\d{1,14}$")


def alter_user_phone(incoming_request: dict) -> bool:
    """
    Update a user's phone number in the mock database after validating
    CSRF token, request format, and phone number syntax.

    Args:
        incoming_request (dict): Dictionary containing HTTP headers and body.
            Expected keys:
                - "headers": dict with a 'X-CSRF-Token' key.
                - "body": JSON string with keys 'user_id' (int) and
                          'new_phone' (str).

    Returns:
        bool: True if the phone number was successfully updated,
              False otherwise.
    """
    try:
        # 1. CSRF token validation
        headers = incoming_request.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            return False

        # 2. Parse and validate request body
        body_str = incoming_request.get("body", "")
        if not body_str:
            return False

        try:
            body = json.loads(body_str)
        except json.JSONDecodeError:
            return False

        user_id = body.get("user_id")
        new_phone = body.get("new_phone")

        if not isinstance(user_id, int) or not isinstance(new_phone, str):
            return False

        # 3. Phone number format check (E.164)
        if not PHONE_REGEX.match(new_phone):
            return False

        # 4. Update the database (mock)
        user_record = database.get(user_id)
        if not user_record:
            return False

        # Perform the update
        user_record["phone"] = new_phone
        return True

    except Exception:
        # In a real application, log the exception details.
        return False