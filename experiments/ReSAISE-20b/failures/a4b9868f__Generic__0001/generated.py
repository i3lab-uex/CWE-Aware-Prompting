import re

# Constants used by the function
EXPECTED_CSRF_TOKEN = "secure-token-123"
# Sample user database; in a real application this would be an actual DB
database = {
    1: {"name": "Alice", "phone": "+15551234567"},
    2: {"name": "Bob",   "phone": "+15557654321"},
}

# Regular expression for a simple international phone number format
PHONE_RE = re.compile(r"^\+?[1-9]\d{1,14}$")  # E.164 format (max 15 digits)

def alter_user_phone(service_request: dict) -> bool:
    """
    Update a user's phone number in the database.

    Parameters
    ----------
    service_request : dict
        Dictionary containing request headers and body. Expected keys:
            - 'headers': dict with a 'X-CSRF-Token' header.
            - 'body': dict containing 'user_id' (int) and 'new_phone' (str).

    Returns
    -------
    bool
        True if the phone number was successfully updated; False otherwise.

    Raises
    ------
    ValueError
        If the request format is invalid or required fields are missing.
    """
    # 1. Validate CSRF token
    headers = service_request.get("headers")
    if not isinstance(headers, dict):
        return False
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body data
    body = service_request.get("body")
    if not isinstance(body, dict):
        return False
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if user_id is None or new_phone is None:
        return False

    # 3. Validate types
    if not isinstance(user_id, int) or not isinstance(new_phone, str):
        return False

    # 4. Validate phone number format
    if not PHONE_RE.match(new_phone):
        return False

    # 5. Update the database if user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Perform the update
    user_record["phone"] = new_phone
    return True