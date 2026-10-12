import re

# Simulated database and expected CSRF token for the application
database = {}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123456"

def modify_user_phone(request_data: dict) -> bool:
    """
    Update a user's phone number in the simulated database after performing
    CSRF validation and basic input sanitization.

    Args:
        request_data (dict): Dictionary containing 'headers' and 'body'.
            Expected structure:
                {
                    "headers": {"CSRF-Token": "<token>"},
                    "body":   {"user_id": <int>, "phone": "<string>"}
                }

    Returns:
        bool: True if the phone number was updated successfully, False otherwise.
    """
    # 1. Validate CSRF token
    headers = request_data.get("headers", {})
    csrf_token = headers.get("CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF validation failed
        return False

    # 2. Extract user ID and phone number from the body
    body = request_data.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_phone = str(body["phone"]).strip()
    except (KeyError, ValueError):
        # Missing or invalid data
        return False

    # 3. Basic phone number validation (simple E.164 or US format)
    # This regex allows optional +, digits only, length 10-15.
    phone_pattern = re.compile(r"^\+?\d{10,15}$")
    if not phone_pattern.match(new_phone):
        # Phone number format is invalid
        return False

    # 4. Check that the user exists in the database
    if user_id not in database:
        # User does not exist
        return False

    # 5. Update the phone number in a safe manner
    try:
        # Store only the sanitized phone string
        database[user_id]["phone"] = new_phone
    except Exception:
        # Unexpected error during update
        return False

    # Successful update
    return True