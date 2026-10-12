import re

# Constants and simulated database (for demonstration purposes)
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"
database = {
    1: {"name": "Alice", "phone": "+15551234567"},
    2: {"name": "Bob",   "phone": "+15557654321"},
}

def _is_valid_phone(phone: str) -> bool:
    """
    Basic phone number validation.
    Accepts numbers with optional leading '+', digits only, length 7-15.
    """
    return bool(re.fullmatch(r"\+?\d{7,15}", phone))

def change_user_phone(payload: dict) -> bool:
    """
    Update a user's phone number after CSRF validation and input checks.

    Args:
        payload (dict): Must contain:
            - headers: dict with 'X-CSRF-Token' key
            - body: dict with 'user_id' (int) and 'new_phone' (str)

    Returns:
        bool: True if update succeeded, False otherwise.
    """
    # 1. CSRF token validation
    headers = payload.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract and validate body data
    body = payload.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if not isinstance(user_id, int) or user_id <= 0:
        return False

    if not isinstance(new_phone, str) or not _is_valid_phone(new_phone):
        return False

    # 3. Update the simulated database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 4. Perform the update
    try:
        user_record["phone"] = new_phone
    except Exception:
        return False

    return True

# Example usage (for testing purposes)
if __name__ == "__main__":
    payload = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_phone": "+15559876543"},
    }
    print(change_user_phone(payload))  # Expected: True
    print(database[1]["phone"])        # Expected: +15559876543