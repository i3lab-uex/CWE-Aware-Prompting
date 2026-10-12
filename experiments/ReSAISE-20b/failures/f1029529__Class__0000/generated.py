import re

# Mock database and expected CSRF token for demonstration purposes
database = {
    1: {"name": "Alice", "phone": "+15551234567"},
    2: {"name": "Bob",   "phone": "+14445556666"},
}
EXPECTED_CSRF_TOKEN = "secure_csrf_token_123"

# Regular expression for a simple E.164 phone number validation
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")

def modify_user_phone(client_request: dict) -> bool:
    """
    Update a user's phone number in the mock database after verifying CSRF token
    and validating input data.

    Args:
        client_request (dict): Request dictionary containing headers and body.
            Expected structure:
                {
                    "headers": {"X-CSRF-Token": "<token>"},
                    "body":   {"user_id": <int>, "new_phone": "<string>"}
                }

    Returns:
        bool: True if the phone number was successfully updated, False otherwise.
    """
    # 1. Verify CSRF token
    headers = client_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid or missing CSRF token
        return False

    # 2. Extract and validate body parameters
    body = client_request.get("body", {})
    user_id_raw = body.get("user_id")
    new_phone_raw = body.get("new_phone")

    # Ensure both parameters are present
    if user_id_raw is None or new_phone_raw is None:
        return False

    # 3. Validate user_id: must be an integer and exist in the database
    try:
        user_id = int(user_id_raw)
    except (ValueError, TypeError):
        return False
    if user_id not in database:
        return False

    # 4. Validate new phone number format
    if not isinstance(new_phone_raw, str) or not PHONE_REGEX.match(new_phone_raw):
        return False

    # 5. Perform the update
    database[user_id]["phone"] = new_phone_raw

    return True