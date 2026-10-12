import re

# Simulated database: user_id -> { "phone": "...", ... }
database = {
    1: {"name": "Alice", "phone": "+15551234567"},
    2: {"name": "Bob",   "phone": "+15557654321"},
}

# Predefined CSRF token that must match the request header
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

# Regular expression for a simple E.164 phone number validation
PHONE_REGEX = re.compile(r"^\+?[1-9]\d{1,14}$")


def modify_user_phone(request_data: dict) -> bool:
    """
    Update a user's phone number after validating the CSRF token and
    ensuring the input data is well-formed.

    Args:
        request_data: A dictionary with keys:
            - 'headers': dict containing the CSRF token under 'X-CSRF-Token'
            - 'body':   dict containing:
                * 'user_id' (int)
                * 'new_phone' (str)

    Returns:
        True if the phone number was updated successfully, False otherwise.
    """
    # 1. Validate presence of headers and body
    if not isinstance(request_data, dict):
        return False

    headers = request_data.get("headers")
    body = request_data.get("body")

    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # 2. CSRF token validation (CWE-352 protection)
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 3. Extract and validate user_id
    try:
        user_id = int(body.get("user_id"))
    except (TypeError, ValueError):
        return False

    # 4. Validate new phone number format
    new_phone = body.get("new_phone")
    if not isinstance(new_phone, str) or not PHONE_REGEX.match(new_phone):
        return False

    # 5. Update the database entry if user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Perform the update
    user_record["phone"] = new_phone
    return True