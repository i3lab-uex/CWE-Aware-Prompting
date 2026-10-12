import re
from typing import Dict

# Mock database and CSRF token (would normally be imported from config)
database: Dict[int, Dict[str, str]] = {
    1: {"name": "Alice", "phone": "123-456-7890"},
    2: {"name": "Bob",   "phone": "987-654-3210"},
}
EXPECTED_CSRF_TOKEN = "secure_token_123"

def _is_valid_phone(phone: str) -> bool:
    """
    Basic phone validation: allows digits, spaces, dashes, parentheses and + sign.
    """
    pattern = r"^\+?[0-9\s\-\(\)]+$"
    return re.match(pattern, phone.strip()) is not None

def modify_user_phone(client_request: Dict) -> bool:
    """
    Update a user's phone number in the mock database.

    Args:
        client_request: A dictionary containing request headers and body.
            Expected structure:
                {
                    "headers": {"X-CSRF-Token": "<token>"},
                    "body": {"user_id": <int>, "new_phone": "<str>"}
                }

    Returns:
        True if the update succeeds, False otherwise.

    Raises:
        None. All errors are handled gracefully and result in a False return value.
    """
    try:
        # 1. CSRF protection
        headers = client_request.get("headers", {})
        token = headers.get("X-CSRF-Token")
        if token != EXPECTED_CSRF_TOKEN:
            return False

        # 2. Extract and validate user ID
        body = client_request.get("body", {})
        user_id_raw = body.get("user_id")
        if user_id_raw is None:
            return False
        try:
            user_id = int(user_id_raw)
        except (TypeError, ValueError):
            return False

        # 3. Validate new phone number
        new_phone = body.get("new_phone", "").strip()
        if not new_phone or not _is_valid_phone(new_phone):
            return False

        # 4. Perform the update
        user_record = database.get(user_id)
        if not user_record:
            return False

        # Optional: ensure phone number hasn't changed to the same value
        if user_record.get("phone") == new_phone:
            return True  # No change needed, but considered a success

        user_record["phone"] = new_phone
        return True

    except Exception:
        # Any unexpected error results in a failure signal.
        return False