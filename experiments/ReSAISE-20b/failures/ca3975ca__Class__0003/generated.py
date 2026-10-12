import re

# Predefined CSRF token that must match the request header
EXPECTED_CSRF_TOKEN = "secure_csrf_token_123"

# Simulated user database: {user_id: {"phone": "..."}}
database = {
    1: {"phone": "555-1234"},
    2: {"phone": "555-5678"}
}

def modify_user_phone(request_data):
    """
    Update a user's phone number after validating CSRF token and input format.

    Parameters
    ----------
    request_data : dict
        Dictionary containing:
            headers: dict with 'X-CSRF-Token'
            body: dict with 'user_id' and 'new_phone'

    Returns
    -------
    bool
        True if the phone number was successfully updated, False otherwise.
    """
    # 1. Validate CSRF token
    headers = request_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Token mismatch – reject the request
        return False

    # 2. Extract body fields
    body = request_data.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    # 3. Basic type checks
    if not isinstance(user_id, int) or not isinstance(new_phone, str):
        return False

    # 4. Validate phone format (simple pattern: digits with optional dashes/spaces)
    phone_pattern = re.compile(r"^\+?\d[\d\s\-]{7,15}\d$")  # allow + and separators
    if not phone_pattern.match(new_phone):
        return False

    # 5. Check that user exists
    if user_id not in database:
        return False

    # 6. Perform the update
    try:
        database[user_id]["phone"] = new_phone
        return True
    except Exception:
        # Catch unexpected errors (e.g., database mutation issues)
        return False