import re

# Mock database and expected CSRF token for this example.
database = {
    1: {"name": "Alice", "phone": "+15551234567"},
    2: {"name": "Bob",   "phone": "+15557654321"},
}
EXPECTED_CSRF_TOKEN = "securetoken123"

# Regular expression for a simple international phone number (E.164 format)
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")


def modify_user_phone(client_request: dict) -> bool:
    """
    Update a user's phone number in the mock database.

    Parameters
    ----------
    client_request : dict
        Dictionary representing an HTTP request. Expected keys:
            - "headers": dict containing the CSRF token under "X-CSRF-Token".
            - "body":   dict with keys "user_id" (int) and "new_phone" (str).

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.
    """
    # 1. Validate request structure
    if not isinstance(client_request, dict):
        return False

    headers = client_request.get("headers", {})
    body = client_request.get("body", {})

    # 2. CSRF token verification
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 3. Extract and validate user ID
    try:
        user_id = int(body.get("user_id"))
    except (TypeError, ValueError):
        return False

    # 4. Validate new phone number format
    new_phone = body.get("new_phone")
    if not isinstance(new_phone, str) or not PHONE_REGEX.match(new_phone):
        return False

    # 5. Perform the update if user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 6. Update phone number
    user_record["phone"] = new_phone
    return True


# Example usage (for testing purposes only)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_phone": "+15559876543"},
    }
    print(modify_user_phone(request))  # Should output: True
    print(database[1]["phone"])        # Should show the updated phone number