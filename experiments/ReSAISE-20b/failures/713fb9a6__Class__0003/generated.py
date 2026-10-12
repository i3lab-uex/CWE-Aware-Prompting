import re

# Simulated user database (user_id -> dict with 'phone' field)
database = {
    1: {"name": "Alice", "phone": "+15551234567"},
    2: {"name": "Bob",   "phone": "+15559876543"},
}

# Expected CSRF token for the session
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

# Regular expression to validate international phone numbers (simple check)
PHONE_REGEX = re.compile(r"^\+?[1-9]\d{1,14}$")  # E.164 format


def change_user_phone(payload: dict) -> bool:
    """
    Update a user's phone number in the simulated database.

    Parameters
    ----------
    payload : dict
        Expected structure:
            {
                "headers": {"X-CSRF-Token": "<token>"},
                "body":   {
                    "user_id": <int>,
                    "new_phone": "<phone string>"
                }
            }

    Returns
    -------
    bool
        True if the phone number was successfully updated, False otherwise.

    Raises
    ------
    ValueError
        If required fields are missing or of incorrect type.
    """

    # 1. CSRF token validation
    headers = payload.get("headers")
    if not isinstance(headers, dict):
        return False

    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract and validate body
    body = payload.get("body")
    if not isinstance(body, dict):
        return False

    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if not isinstance(user_id, int) or user_id <= 0:
        return False

    if not isinstance(new_phone, str):
        return False

    # 3. Phone format validation (E.164)
    if not PHONE_REGEX.match(new_phone):
        return False

    # 4. Update database entry
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Perform the update atomically
    try:
        user_record["phone"] = new_phone
    except Exception:
        return False

    return True


# Example usage (for testing purposes only)
if __name__ == "__main__":
    test_payload = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_phone": "+15557654321"},
    }
    print(change_user_phone(test_payload))  # Expected: True
    print(database[1]["phone"])            # Updated phone number