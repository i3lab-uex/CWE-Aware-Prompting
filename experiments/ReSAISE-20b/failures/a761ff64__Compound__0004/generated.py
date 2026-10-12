import re

# Simulated database of users: user_id -> { "phone": str, ... }
database = {}

# Predefined CSRF token that must be present in the request headers
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

# Regular expression to validate international phone numbers (basic check)
PHONE_REGEX = re.compile(r"^\+?[1-9]\d{1,14}$")


def alter_user_phone(input: dict) -> bool:
    """
    Update the phone number of a user in the simulated database.

    Args:
        input (dict): Request dictionary containing headers and body.
            Expected structure:
                {
                    "headers": {"X-CSRF-Token": "..."},
                    "body":   {"user_id": "<id>", "new_phone": "+1234567890"}
                }

    Returns:
        bool: True if the update succeeded, False otherwise.

    Raises:
        ValueError: If required fields are missing or invalid.
    """
    # 1. Validate CSRF token
    headers = input.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Reject request due to missing/incorrect CSRF token
        return False

    # 2. Extract body parameters
    body = input.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if not user_id or not new_phone:
        return False

    # 3. Validate phone number format
    if not PHONE_REGEX.match(new_phone):
        return False

    # 4. Perform the update in the database
    user_record = database.get(user_id)
    if not user_record:
        # User does not exist
        return False

    # Update phone number safely
    user_record["phone"] = new_phone
    return True


# Example usage (for testing purposes only)
if __name__ == "__main__":
    # Seed database
    database["user123"] = {"phone": "+1112223333", "name": "Alice"}

    # Valid request
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": "user123", "new_phone": "+15551234567"}
    }
    print(alter_user_phone(req))          # True
    print(database["user123"]["phone"])   # +15551234567

    # Invalid CSRF token
    bad_req = {
        "headers": {"X-CSRF-Token": "bad-token"},
        "body": {"user_id": "user123", "new_phone": "+15551234567"}
    }
    print(alter_user_phone(bad_req))      # False