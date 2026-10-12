import re

# Sample database and CSRF token for demonstration purposes
database = {
    1: {"name": "Alice", "phone": "+15551234567"},
    2: {"name": "Bob",   "phone": "+15559876543"}
}
EXPECTED_CSRF_TOKEN = "secure_token_123"

# Regular expression for a basic E.164 phone number format
PHONE_REGEX = re.compile(r"^\+?[1-9]\d{1,14}$")


def alter_user_phone(service_request: dict) -> bool:
    """
    Update a user's phone number after verifying CSRF token and validating input.

    Parameters
    ----------
    service_request : dict
        Dictionary containing 'headers' and 'body'. The body must include:
            - 'user_id': int
            - 'new_phone': str

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    # 1. CSRF token validation
    headers = service_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract payload
    body = service_request.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_phone = str(body["new_phone"]).strip()
    except (KeyError, ValueError):
        return False

    # 3. Validate phone number format
    if not PHONE_REGEX.match(new_phone):
        return False

    # 4. Ensure user exists
    if user_id not in database:
        return False

    # 5. Perform the update
    try:
        database[user_id]["phone"] = new_phone
        return True
    except Exception:
        # Catch unexpected errors to avoid leaking sensitive info
        return False