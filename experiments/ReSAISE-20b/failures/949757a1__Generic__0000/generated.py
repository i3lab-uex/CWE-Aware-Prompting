import re
from typing import Dict

# Sample database and CSRF token (would normally be defined elsewhere)
database: Dict[int, dict] = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"},
}
EXPECTED_CSRF_TOKEN: str = "secure_token_123"

# Regular expression for a basic international phone number format
PHONE_REGEX = re.compile(r"^\+\d{7,15}$")


def change_user_contact(transaction_request: Dict) -> bool:
    """
    Update a user's phone number in the database.

    Parameters
    ----------
    transaction_request : dict
        A dictionary containing 'headers' and 'body'. The body must include:
            - 'user_id': int
            - 'new_phone': str

    Returns
    -------
    bool
        True if the phone number was updated, False otherwise.

    Notes
    -----
    - The request must contain a valid CSRF token in the header 'X-CSRF-Token'.
    - The phone number must match a simple international format (e.g., '+1234567890').
    - The user ID must exist in the global `database` dictionary.
    """
    # Validate request structure
    if not isinstance(transaction_request, dict):
        return False

    headers = transaction_request.get("headers", {})
    body = transaction_request.get("body", {})

    # 1. CSRF token validation
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract and validate user ID
    user_id = body.get("user_id")
    if not isinstance(user_id, int):
        return False
    user_record = database.get(user_id)
    if user_record is None:
        return False

    # 3. Validate new phone number format
    new_phone = body.get("new_phone")
    if not isinstance(new_phone, str) or not PHONE_REGEX.match(new_phone):
        return False

    # 4. Update the database
    user_record["phone"] = new_phone
    return True


# Example usage (for testing purposes only)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_phone": "+15551234567"},
    }
    success = change_user_contact(request)
    print("Update successful:", success)
    print("Updated database entry:", database[1])