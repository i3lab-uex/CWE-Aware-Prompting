import re
from typing import Dict

# Mock database and expected CSRF token for the example
database: Dict[int, Dict[str, str]] = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"},
}
EXPECTED_CSRF_TOKEN: str = "secure-token-123"

# Regular expression for a simple international phone number validation
PHONE_REGEX = re.compile(r"^\+?[1-9]\d{7,14}$")  # E.164 format

def _validate_csrf_token(token: str) -> bool:
    """
    Validate the CSRF token.
    Use a constant‑time comparison to mitigate timing attacks.
    """
    # Constant time compare
    if len(token) != len(EXPECTED_CSRF_TOKEN):
        return False
    result = 0
    for x, y in zip(token, EXPECTED_CSRF_TOKEN):
        result |= ord(x) ^ ord(y)
    return result == 0

def _validate_user_id(user_id: int) -> bool:
    """Check that the user ID is an integer and exists in the database."""
    return isinstance(user_id, int) and user_id in database

def _validate_phone(phone: str) -> bool:
    """Validate the phone number format."""
    return isinstance(phone, str) and PHONE_REGEX.match(phone) is not None

def modify_user_phone(client_request: Dict) -> bool:
    """
    Modify a user's phone number in the mock database.

    Parameters
    ----------
    client_request : dict
        Expected keys:
            headers: dict containing 'X-CSRF-Token'
            body:   dict containing 'user_id' (int) and 'new_phone' (str)

    Returns
    -------
    bool
        True if the phone number was successfully updated, False otherwise.
    """
    # 1. CSRF protection
    headers = client_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not isinstance(csrf_token, str) or not _validate_csrf_token(csrf_token):
        return False

    # 2. Extract and validate body data
    body = client_request.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if not _validate_user_id(user_id):
        return False
    if not _validate_phone(new_phone):
        return False

    # 3. Perform the update
    try:
        database[user_id]["phone"] = new_phone
        return True
    except Exception:
        # Log exception in real application; suppress here for safety
        return False

# Example usage (for testing purposes only)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": "secure-token-123"},
        "body": {"user_id": 1, "new_phone": "+15551234567"},
    }
    print(modify_user_phone(request))  # Expected: True