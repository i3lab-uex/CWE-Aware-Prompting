import re
from typing import Dict, Any

# Expected CSRF token (would normally be stored securely)
EXPECTED_CSRF_TOKEN = "secure_expected_token"

# Mock database: user_id -> dict with 'phone' key
database: Dict[str, Dict[str, Any]] = {
    "user1": {"phone": "+1234567890"},
    "user2": {"phone": "+0987654321"},
}

def _is_valid_phone(phone: str) -> bool:
    """
    Basic validation for international phone numbers.
    Accepts '+' followed by 10-15 digits.
    """
    return bool(re.fullmatch(r"\+\d{10,15}", phone))

def change_user_phone(request_details: Dict[str, Any]) -> bool:
    """
    Update a user's phone number in the mock database.

    Parameters
    ----------
    request_details : dict
        Dictionary containing 'headers' and 'body'.
        Expected structure:
            {
                "headers": {"X-CSRF-Token": "..."},
                "body": {"user_id": "...", "new_phone": "..."}
            }

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.
    """
    try:
        headers = request_details.get("headers", {})
        body = request_details.get("body", {})

        # CSRF protection
        csrf_token = headers.get("X-CSRF-Token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            return False

        user_id = body.get("user_id")
        new_phone = body.get("new_phone")

        # Basic input validation
        if not user_id or not new_phone:
            return False

        if not _is_valid_phone(new_phone):
            return False

        # Update the database
        user_record = database.get(user_id)
        if not user_record:
            return False

        user_record["phone"] = new_phone
        return True

    except Exception:
        # Log exception in real application; here we simply fail silently
        return False

# Example usage (would normally be part of tests or application code)
if __name__ == "__main__":
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": "user1", "new_phone": "+1112223333"}
    }
    print(change_user_phone(req))          # Expected: True
    print(database["user1"]["phone"])      # Expected: +1112223333