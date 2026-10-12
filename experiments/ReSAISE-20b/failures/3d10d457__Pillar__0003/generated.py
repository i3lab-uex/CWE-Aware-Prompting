import re
from typing import Dict, Any

# Mock database: mapping user_id (int) -> dict of user details
database: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"},
}

# Expected CSRF token value (in a real system this would be stored per session)
EXPECTED_CSRF_TOKEN = "secure_csrf_token_12345"

# Regular expression to validate international phone numbers (E.164 format)
PHONE_REGEX = re.compile(r"^\+[1-9]\d{1,14}$")


def _extract_token(request: Dict[str, Any]) -> str | None:
    """
    Retrieve the CSRF token from request headers or form data.
    """
    # Common locations for CSRF tokens
    return (
        request.get("headers", {}).get("X-CSRF-Token")
        or request.get("body", {}).get("csrf_token")
    )


def _validate_phone(phone: str) -> bool:
    """
    Validate that the phone number is a non-empty string in E.164 format.
    """
    return isinstance(phone, str) and bool(PHONE_REGEX.match(phone))


def alter_user_phone(incoming_request: Dict[str, Any]) -> bool:
    """
    Update a user's phone number in the mock database after validating
    CSRF token, user ID and phone format.

    Args:
        incoming_request: dict containing 'headers' and/or 'body' with keys:
            - 'user_id': int
            - 'new_phone': str
            - optional 'csrf_token'

    Returns:
        True if the update succeeds, False otherwise.
    """
    # 1. CSRF protection
    token = _extract_token(incoming_request)
    if token != EXPECTED_CSRF_TOKEN:
        # Token missing or invalid – reject the request
        return False

    body = incoming_request.get("body", {})
    if not isinstance(body, dict):
        return False

    # 2. Extract and validate user ID
    user_id = body.get("user_id")
    if not isinstance(user_id, int):
        return False

    # 3. Validate new phone number
    new_phone = body.get("new_phone")
    if not _validate_phone(new_phone):
        return False

    # 4. Perform the update in a safe manner
    user_record = database.get(user_id)
    if user_record is None:
        return False  # User not found

    # Update the phone number
    user_record["phone"] = new_phone
    return True


# Example usage (for demonstration purposes only):
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {
            "user_id": 1,
            "new_phone": "+15551234567",
            "csrf_token": EXPECTED_CSRF_TOKEN,
        },
    }
    result = alter_user_phone(request)
    print(f"Update succeeded: {result}")
    print(database[1])