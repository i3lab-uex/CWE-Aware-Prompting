import re
from typing import Dict

# Simulated database and CSRF token (would normally be stored securely)
database: Dict[int, Dict[str, str]] = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"},
}
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token-123"

# Regular expression for a simple E.164 phone number validation
PHONE_REGEX = re.compile(r"^\+?[1-9]\d{1,14}$")


def update_user_phone(request: Dict) -> bool:
    """
    Update the phone number for a user.

    Parameters
    ----------
    request : dict
        Expected keys:
            headers : dict
                Must contain 'X-CSRF-Token' matching EXPECTED_CSRF_TOKEN.
            body : dict
                Must contain 'user_id' (int) and 'new_phone' (str).

    Returns
    -------
    bool
        True if the phone number was updated, False otherwise.
    """
    # 1. CSRF token validation
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body parameters
    body = request.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if not isinstance(user_id, int) or not isinstance(new_phone, str):
        return False

    # 3. Validate phone number format
    if not PHONE_REGEX.match(new_phone):
        return False

    # 4. Update the database record if user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Simulate atomic update
    try:
        database[user_id]["phone"] = new_phone
        return True
    except Exception:
        # In a real scenario, log the exception and rollback if necessary
        return False


# Example usage (for testing purposes only)
if __name__ == "__main__":
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_phone": "+15551234567"},
    }
    print(update_user_phone(req))  # Expected: True
    print(database[1]["phone"])   # Expected: +15551234567