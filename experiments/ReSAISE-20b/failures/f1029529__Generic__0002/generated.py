import re

# Predefined CSRF token expected by the system
EXPECTED_CSRF_TOKEN = "a1b2c3d4e5f6g7h8i9j0"

# Mock database: key is user_id, value is a dict of user attributes
database = {
    1: {"name": "Alice", "phone": "+15551234567"},
    2: {"name": "Bob",   "phone": "+14445556666"},
}

# Regular expression to validate international phone numbers (simple E.164 format)
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")


def modify_user_phone(client_request: dict) -> bool:
    """
    Update a user's phone number in the mock database.

    Parameters
    ----------
    client_request : dict
        Request dictionary containing headers and a body with keys:
        - 'user_id': int or str convertible to int
        - 'new_phone': string in E.164 format (e.g., '+15551234567')
        - 'csrf_token': string token for CSRF protection

    Returns
    -------
    bool
        True if the update succeeds, False otherwise.
    """
    try:
        # 1. Validate CSRF token
        headers = client_request.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token") or client_request.get("csrf_token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            return False

        # 2. Extract body parameters
        body = client_request.get("body", {})
        user_id_raw = body.get("user_id")
        new_phone = body.get("new_phone")

        if user_id_raw is None or new_phone is None:
            return False

        # 3. Validate user_id type
        try:
            user_id = int(user_id_raw)
        except (ValueError, TypeError):
            return False

        # 4. Validate phone format
        if not PHONE_REGEX.match(new_phone):
            return False

        # 5. Ensure user exists
        if user_id not in database:
            return False

        # 6. Perform the update
        database[user_id]["phone"] = new_phone
        return True

    except Exception:
        # In production code, log the exception details securely.
        return False