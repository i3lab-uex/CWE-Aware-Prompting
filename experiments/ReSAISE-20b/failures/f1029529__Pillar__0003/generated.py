import re

# Constants for CSRF protection
EXPECTED_CSRF_TOKEN = "secure_expected_token"

# Mock database: user_id -> user record dict
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"},
}

# Regular expression for a simple E.164 phone number validation
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")

def modify_user_phone(client_request: dict) -> bool:
    """
    Update a user's phone number after validating CSRF token, user existence,
    and phone format.

    Parameters
    ----------
    client_request : dict
        Expected structure:
            {
                "headers": {"X-CSRF-Token": "<token>"},
                "body":   {
                    "user_id" : <int>,
                    "new_phone": "<string>"
                }
            }

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    try:
        # 1. CSRF protection
        headers = client_request.get("headers", {})
        token = headers.get("X-CSRF-Token")
        if token != EXPECTED_CSRF_TOKEN:
            # CSRF check failed
            return False

        # 2. Extract payload
        body = client_request.get("body", {})
        user_id = body.get("user_id")
        new_phone = body.get("new_phone")

        if not isinstance(user_id, int) or not isinstance(new_phone, str):
            return False

        # 3. Validate phone format
        if not PHONE_REGEX.match(new_phone):
            return False

        # 4. Check user exists
        user_record = database.get(user_id)
        if not user_record:
            return False

        # 5. Perform the update
        user_record["phone"] = new_phone
        return True

    except Exception:
        # In a real application we would log the exception.
        # For security, do not expose internal errors to callers.
        return False