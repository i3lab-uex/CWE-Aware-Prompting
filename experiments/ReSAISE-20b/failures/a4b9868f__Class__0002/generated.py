import re

# Preconfigured CSRF token (in a real app this would be stored securely)
EXPECTED_CSRF_TOKEN = "securetoken123"

# Sample user database: user_id -> phone number
database = {
    1: "555-1234",
    2: "555-5678",
    3: "555-9012"
}

# Regular expression for a simple international phone number (e.g., +1234567890 or 123-456-7890)
PHONE_REGEX = re.compile(r"^\+?\d{1,3}[-\s]?(?:\(\d+\)|\d+)[-\s]?\d{3,4}[-\s]?\d{4}$")


def _validate_csrf(headers: dict) -> bool:
    """
    Verify that the request contains a valid CSRF token.
    The token may be sent in headers or as part of the body; we check both for flexibility.
    """
    token = headers.get("X-CSRF-Token") or headers.get("csrf_token")
    return token == EXPECTED_CSRF_TOKEN


def _validate_phone_number(phone: str) -> bool:
    """
    Basic validation to ensure the phone number follows a reasonable pattern.
    This is not exhaustive but protects against obvious malformed inputs.
    """
    return bool(PHONE_REGEX.fullmatch(phone))


def alter_user_phone(service_request: dict) -> bool:
    """
    Update a user's phone number in the database.

    Parameters
    ----------
    service_request : dict
        A dictionary containing 'headers' and 'body'.  The body must include:
            - 'user_id': int
            - 'new_phone': str

    Returns
    -------
    bool
        True if the phone number was updated successfully; False otherwise.
    """
    # Basic input validation
    if not isinstance(service_request, dict):
        return False

    headers = service_request.get("headers", {})
    body = service_request.get("body", {})

    # 1. CSRF token validation
    if not _validate_csrf(headers):
        return False

    # 2. Extract required fields
    try:
        user_id = int(body["user_id"])
        new_phone = str(body["new_phone"]).strip()
    except (KeyError, ValueError, TypeError):
        return False

    # 3. Validate phone number format
    if not _validate_phone_number(new_phone):
        return False

    # 4. Check that the user exists
    if user_id not in database:
        return False

    # 5. Update the phone number
    database[user_id] = new_phone
    return True

# Example usage (for testing purposes)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 2, "new_phone": "+1-800-555-0199"}
    }
    result = alter_user_phone(request)
    print("Update successful:", result)  # Should output: Update successful: True
    print("New database state:", database)