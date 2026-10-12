import re

# Sample database and CSRF token for the application
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+0987654321"}
}
EXPECTED_CSRF_TOKEN = "secure-token-12345"

# Regular expression for a basic E.164 phone number format
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")

def alter_user_phone(service_request: dict) -> bool:
    """
    Update a user's phone number in the database after validating the CSRF token
    and ensuring that the provided data is well‑formed.

    Parameters
    ----------
    service_request : dict
        Dictionary containing a 'headers' key with request headers and a
        'body' key with the payload. The body must contain:
            - 'user_id': int
            - 'new_phone': str

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.
    """

    # 1. Validate CSRF token
    headers = service_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract and validate payload
    body = service_request.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_phone = str(body["new_phone"]).strip()
    except (KeyError, ValueError, TypeError):
        return False

    # 3. Validate phone number format
    if not PHONE_REGEX.match(new_phone):
        return False

    # 4. Update the database if user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 5. Perform the update
    user_record["phone"] = new_phone
    return True