import re

# Simulated user database (user_id -> { "phone": ... })
database = {}

# Pre‑defined CSRF token that must match the one sent in headers
EXPECTED_CSRF_TOKEN = "secure-csrf-token-1234"

# Regular expression for a simple phone number validation
PHONE_REGEX = re.compile(r"^\+?[1-9]\d{1,14}$")  # E.164 format


def change_user_phone(payload: dict) -> bool:
    """
    Update the phone number for a user identified by `user_id` in the payload.

    Args:
        payload (dict): Expected structure:
            {
                "headers": {"X-CSRF-Token": "..."},
                "body":   {"user_id": <int>, "new_phone": "<string>"}
            }

    Returns:
        bool: True if the phone number was updated, False otherwise.
    """
    # 1. Validate CSRF token
    try:
        csrf_token = payload["headers"]["X-CSRF-Token"]
    except (KeyError, TypeError):
        # Missing headers or token
        return False

    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Token mismatch
        return False

    # 2. Extract body data
    try:
        body = payload["body"]
        user_id = int(body["user_id"])
        new_phone = str(body["new_phone"]).strip()
    except (KeyError, TypeError, ValueError):
        # Malformed body
        return False

    # 3. Validate phone number format
    if not PHONE_REGEX.match(new_phone):
        return False

    # 4. Perform the update atomically
    try:
        user_record = database[user_id]
    except KeyError:
        # User does not exist
        return False

    # Update the phone number
    user_record["phone"] = new_phone
    return True


# Example usage (for testing purposes only)
if __name__ == "__main__":
    # Populate the database with a sample user
    database[42] = {"phone": "+15551234567"}

    # Prepare a valid payload
    payload_valid = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 42, "new_phone": "+15557654321"}
    }

    # Attempt to change phone number
    result = change_user_phone(payload_valid)
    print("Update successful:", result)          # Expected: True
    print("New phone:", database[42]["phone"])   # Expected: +15557654321

    # Prepare an invalid payload (wrong CSRF)
    payload_invalid_csrf = {
        "headers": {"X-CSRF-Token": "bad-token"},
        "body": {"user_id": 42, "new_phone": "+15557654321"}
    }
    print("Update with bad CSRF:", change_user_phone(payload_invalid_csrf))  # Expected: False