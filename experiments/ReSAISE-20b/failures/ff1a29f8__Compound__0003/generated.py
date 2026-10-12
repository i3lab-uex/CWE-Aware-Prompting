import re

# Mock database and CSRF token for the example
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"},
}
EXPECTED_CSRF_TOKEN = "secure_token_123"

def _is_valid_phone(phone: str) -> bool:
    """
    Very simple phone number validation.
    Accepts optional leading '+', followed by 10-15 digits.
    """
    pattern = r"^\+?\d{10,15}$"
    return re.match(pattern, phone) is not None

def change_user_phone(request_details: dict) -> bool:
    """
    Update a user's phone number in the mock database.

    Parameters
    ----------
    request_details : dict
        Expected to contain:
            - headers: dict with 'X-CSRF-Token'
            - body: dict with 'user_id' (int) and 'new_phone' (str)

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    # 1. CSRF protection: ensure token matches expected value
    headers = request_details.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract payload
    body = request_details.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    # 3. Basic validation of inputs
    if not isinstance(user_id, int) or user_id <= 0:
        return False

    if not isinstance(new_phone, str) or not _is_valid_phone(new_phone):
        return False

    # 4. Update the database if user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 5. Perform the update
    user_record["phone"] = new_phone
    return True

# Example usage:
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": "secure_token_123"},
        "body":    {"user_id": 1, "new_phone": "+1122334455"}
    }
    print(change_user_phone(request))  # Expected: True
    print(database[1]["phone"])        # Updated phone number