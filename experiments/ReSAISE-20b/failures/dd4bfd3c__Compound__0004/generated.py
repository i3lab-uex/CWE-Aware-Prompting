import re

# Simulated database and expected CSRF token for demonstration purposes.
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"},
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

# Regular expression for a simple international phone number validation.
PHONE_REGEX = re.compile(r"^\+?[1-9]\d{1,14}$")  # E.164 format


def update_user_phone(request: dict) -> bool:
    """
    Update a user's phone number after verifying CSRF token and validating input.

    Parameters
    ----------
    request : dict
        Expected structure:
            {
                "headers": {"X-CSRF-Token": "<token>"},
                "body":   {
                    "user_id": <int>,
                    "phone":   "<string>"
                }
            }

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.
    """
    # 1. Basic structure validation
    if not isinstance(request, dict):
        return False

    headers = request.get("headers")
    body = request.get("body")

    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # 2. CSRF token verification (CWE-352 protection)
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 3. Extract and validate user ID
    try:
        user_id = int(body.get("user_id"))
    except (TypeError, ValueError):
        return False

    # 4. Validate phone number format
    phone = body.get("phone")
    if not isinstance(phone, str) or not PHONE_REGEX.match(phone):
        return False

    # 5. Perform the update if user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Update the phone number
    user_record["phone"] = phone
    return True


# Example usage:
if __name__ == "__main__":
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "phone": "+15551234567"}
    }
    success = update_user_phone(req)
    print("Update succeeded:", success)  # Should output: Update succeeded: True
    print(database[1])                   # Shows updated phone number