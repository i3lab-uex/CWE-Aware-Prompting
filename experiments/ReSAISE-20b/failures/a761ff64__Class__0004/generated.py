import re

# Simulated database: {user_id: {"phone": "123-456-7890", ...}}
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"}
}

# Predefined CSRF token
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

# Regular expression for a simple international phone number validation
PHONE_REGEX = re.compile(r"^\+?\d{7,15}$")


def alter_user_phone(input: dict) -> bool:
    """
    Update a user's phone number after validating CSRF token and input data.

    Args:
        input (dict): Request dictionary containing:
            - headers: dict with 'X-CSRF-Token'
            - body:   dict with keys:
                * user_id (int)
                * new_phone (str)

    Returns:
        bool: True if the update succeeded, False otherwise.

    Raises:
        ValueError: If required fields are missing or invalid.
    """
    # 1. Validate presence of headers and CSRF token
    headers = input.get("headers")
    if not isinstance(headers, dict):
        raise ValueError("Missing or invalid headers")

    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Token mismatch: treat as failure (do not leak details)
        return False

    # 2. Extract body
    body = input.get("body")
    if not isinstance(body, dict):
        raise ValueError("Missing or invalid body")

    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError("Invalid or missing user_id")

    if not isinstance(new_phone, str) or not PHONE_REGEX.match(new_phone):
        raise ValueError("Invalid phone number format")

    # 3. Update the database atomically
    user_record = database.get(user_id)
    if not user_record:
        # User does not exist
        return False

    # Preserve other fields; only update phone
    user_record["phone"] = new_phone
    return True


# Example usage:
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_phone": "+15551234567"}
    }
    success = alter_user_phone(request)
    print("Update successful:", success)
    print("New database state:", database[1])