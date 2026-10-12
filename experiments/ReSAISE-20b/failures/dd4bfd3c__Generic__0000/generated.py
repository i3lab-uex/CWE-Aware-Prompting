import re

# Simulated database and CSRF token for demonstration purposes.
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"},
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

# Regular expression for a simple international phone number validation.
PHONE_REGEX = re.compile(r"^\+?[1-9]\d{1,14}$")


def update_user_phone(request: dict) -> bool:
    """
    Update the phone number of a user.

    Parameters
    ----------
    request : dict
        The request object containing:
            - headers: dict, must contain 'X-CSRF-Token'
            - body:   dict, must contain 'user_id' and 'new_phone'

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.
    """
    # 1. CSRF token validation
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body data
    body = request.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    # 3. Basic input validation
    if not isinstance(user_id, int) or user_id <= 0:
        return False

    if not isinstance(new_phone, str) or not PHONE_REGEX.match(new_phone):
        return False

    # 4. Update the database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 5. Perform the update
    user_record["phone"] = new_phone
    return True

# Example usage (for testing purposes only)
if __name__ == "__main__":
    sample_request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_phone": "+15551234567"},
    }
    result = update_user_phone(sample_request)
    print("Update successful:", result)
    print("Updated record:", database[1])