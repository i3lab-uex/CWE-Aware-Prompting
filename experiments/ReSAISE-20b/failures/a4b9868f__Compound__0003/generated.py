import re

# Sample database: user_id -> {'phone': str, ...}
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"},
}

# Preconfigured CSRF token
EXPECTED_CSRF_TOKEN = "secure_csrf_token_123"

# Regular expression for validating international phone numbers
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")

def alter_user_phone(service_request: dict) -> bool:
    """
    Update the phone number of a user.

    Parameters
    ----------
    service_request : dict
        Must contain:
            - 'headers': dict with a 'X-CSRF-Token' key.
            - 'body': dict with keys 'user_id' (int) and 'new_phone' (str).

    Returns
    -------
    bool
        True if the phone number was updated, False otherwise.
    """
    try:
        # 1. Validate CSRF token
        headers = service_request.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            return False

        # 2. Extract and validate body
        body = service_request.get("body", {})
        user_id = body.get("user_id")
        new_phone = body.get("new_phone")

        # Basic type checks
        if not isinstance(user_id, int) or user_id <= 0:
            return False
        if not isinstance(new_phone, str):
            return False

        # Phone number format validation
        if not PHONE_REGEX.match(new_phone):
            return False

        # 3. Check user existence
        if user_id not in database:
            return False

        # 4. Update phone number
        database[user_id]["phone"] = new_phone
        return True

    except Exception:
        # In a real application, log the exception securely.
        return False