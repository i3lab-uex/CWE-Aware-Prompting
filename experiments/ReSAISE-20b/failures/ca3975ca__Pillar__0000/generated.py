import re

# Simulated database: user_id -> dict of user attributes
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"},
}

# Expected CSRF token for validation
EXPECTED_CSRF_TOKEN = "secure-token-12345"

# Regular expression to validate international phone numbers (simple pattern)
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")


def modify_user_phone(request_data: dict) -> bool:
    """
    Update the phone number of a user in the simulated database.

    Parameters
    ----------
    request_data : dict
        Dictionary containing:
            - headers: {'X-CSRF-Token': str}
            - body   : {'user_id': int, 'new_phone': str}

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.

    Raises
    ------
    ValueError
        If required fields are missing or the CSRF token is invalid.
    """
    # 1. Validate presence of headers and body
    if not isinstance(request_data, dict):
        raise ValueError("Request data must be a dictionary.")

    headers = request_data.get("headers")
    body   = request_data.get("body")

    if not headers or not isinstance(headers, dict):
        raise ValueError("Missing or invalid 'headers' in request data.")
    if not body or not isinstance(body, dict):
        raise ValueError("Missing or invalid 'body' in request data.")

    # 2. CSRF protection
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Reject the request due to CSRF mismatch
        return False

    # 3. Extract user_id and new_phone from body
    try:
        user_id = int(body["user_id"])
        new_phone = str(body["new_phone"]).strip()
    except (KeyError, TypeError, ValueError):
        # Missing or malformed fields
        return False

    # 4. Validate phone number format (basic international check)
    if not PHONE_REGEX.match(new_phone):
        return False

    # 5. Check that the user exists in the database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 6. Update the phone number atomically (simulated)
    user_record["phone"] = new_phone
    return True


# Example usage (uncomment to test)
# request = {
#     "headers": {"X-CSRF-Token": "secure-token-12345"},
#     "body"   : {"user_id": 1, "new_phone": "+15551234567"}
# }
# print(modify_user_phone(request))  # Expected: True