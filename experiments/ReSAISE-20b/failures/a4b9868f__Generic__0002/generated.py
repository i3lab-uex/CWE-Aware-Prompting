import re

# Sample context (would normally be provided by the surrounding application)
database = {
    1: {"name": "Alice", "phone": "+15551234567"},
    2: {"name": "Bob",   "phone": "+15557654321"}
}
EXPECTED_CSRF_TOKEN = "secure_token_12345"

# Regular expression for a simple E.164 phone number validation
PHONE_REGEX = re.compile(r"^\+?[1-9]\d{1,14}$")

def alter_user_phone(service_request: dict) -> bool:
    """
    Update a user's phone number in the database.

    Parameters
    ----------
    service_request : dict
        Dictionary containing request headers and body. Expected structure:
            {
                "headers": {"X-CSRF-Token": "<token>"},
                "body":    {"user_id": <int>, "new_phone": "<string>"}
            }

    Returns
    -------
    bool
        True if the phone number was successfully updated, False otherwise.
    """
    # 1. Validate CSRF token
    headers = service_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body data
    body = service_request.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    # 3. Validate input types
    if not isinstance(user_id, int) or not isinstance(new_phone, str):
        return False

    # 4. Validate phone number format
    if not PHONE_REGEX.match(new_phone):
        return False

    # 5. Update the database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Optional: check that the new phone is different
    if user_record.get("phone") == new_phone:
        return True  # no change needed, but considered successful

    user_record["phone"] = new_phone
    return True