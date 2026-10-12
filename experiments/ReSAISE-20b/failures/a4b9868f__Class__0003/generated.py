import re
import hmac

# Sample user database: {user_id: {"phone": "<current phone>"}, ...}
database = {
    1: {"phone": "555-1234"},
    2: {"phone": "555-5678"}
}

# Preconfigured CSRF token
EXPECTED_CSRF_TOKEN = "s3cureT0k3n"

# Regular expression for a basic phone number (digits, optional dashes/parentheses/spaces)
PHONE_REGEX = re.compile(r"^\+?\d[\d\s\-\(\)]{7,}\d$")

def _is_valid_phone(phone: str) -> bool:
    """Validate phone number format."""
    return bool(PHONE_REGEX.match(phone))

def alter_user_phone(service_request: dict) -> bool:
    """
    Update the phone number of a user.

    Parameters
    ----------
    service_request : dict
        Expected to contain:
            headers: dict with 'X-CSRF-Token' key.
            body   : dict with 'user_id' and 'new_phone'.

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.
    """
    # 1. CSRF token validation (constant-time comparison)
    headers = service_request.get("headers", {})
    token = headers.get("X-CSRF-Token")
    if not token or not hmac.compare_digest(token, EXPECTED_CSRF_TOKEN):
        return False

    # 2. Extract user ID and new phone from body
    body = service_request.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_phone = body["new_phone"]
    except (KeyError, ValueError, TypeError):
        return False

    # 3. Validate phone number format
    if not _is_valid_phone(new_phone):
        return False

    # 4. Verify user exists
    if user_id not in database:
        return False

    # 5. Update phone number
    try:
        database[user_id]["phone"] = new_phone
        return True
    except Exception:
        # Catch unexpected errors (e.g., database lock, permission issues)
        return False