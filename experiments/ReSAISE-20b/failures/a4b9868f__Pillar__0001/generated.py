import re

# Sample user database (user_id -> user data)
database = {
    1: {"name": "Alice", "phone": "+15551234567"},
    2: {"name": "Bob",   "phone": "+15559876543"},
}

# Preconfigured CSRF token
EXPECTED_CSRF_TOKEN = "s3cr3t-csrf-token"

# Regular expression to validate E.164 phone numbers (e.g., +15551234567)
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")


def alter_user_phone(service_request: dict) -> bool:
    """
    Update a user's phone number after validating CSRF token and input format.

    Args:
        service_request (dict): Contains 'headers' and 'body'.
            Expected structure:
                {
                    "headers": {"X-CSRF-Token": "<token>"},
                    "body":    {"user_id": <int>, "phone": "<string>"}
                }

    Returns:
        bool: True if update succeeded, False otherwise.
    """
    # 1. CSRF protection
    try:
        csrf_token = service_request["headers"]["X-CSRF-Token"]
    except (KeyError, TypeError):
        return False
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract and validate body payload
    try:
        body = service_request["body"]
        user_id = int(body["user_id"])
        new_phone = body["phone"].strip()
    except (KeyError, TypeError, ValueError):
        return False

    # 3. Validate phone number format
    if not PHONE_REGEX.match(new_phone):
        return False

    # 4. Update database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Perform the update atomically
    user_record["phone"] = new_phone
    return True