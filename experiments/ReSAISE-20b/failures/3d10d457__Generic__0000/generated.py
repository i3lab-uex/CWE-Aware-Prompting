import re

# Mock database and CSRF token (for demonstration purposes)
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+0987654321"},
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

# Regular expression to validate international phone numbers (basic)
PHONE_REGEX = re.compile(r"^\+?[1-9]\d{1,14}$")  # E.164 format


def alter_user_phone(incoming_request: dict) -> bool:
    """
    Update a user's phone number in the mock database.

    Parameters
    ----------
    incoming_request : dict
        Expected structure:
            {
                "headers": {"X-CSRF-Token": "..."},
                "body": {"user_id": int, "phone_number": str}
            }

    Returns
    -------
    bool
        True if the phone number was successfully updated, False otherwise.
    """
    # 1. Validate CSRF token
    headers = incoming_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body parameters
    body = incoming_request.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_phone = str(body["phone_number"]).strip()
    except (KeyError, ValueError):
        return False

    # 3. Validate phone number format
    if not PHONE_REGEX.match(new_phone):
        return False

    # 4. Check that the user exists in the database
    if user_id not in database:
        return False

    # 5. Update the phone number
    try:
        database[user_id]["phone"] = new_phone
        return True
    except Exception:
        # In a real application, log the exception
        return False


# Example usage (for testing only)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "phone_number": "+11234567890"},
    }
    result = alter_user_phone(request)
    print("Update succeeded:", result)
    print("Updated record:", database[1])