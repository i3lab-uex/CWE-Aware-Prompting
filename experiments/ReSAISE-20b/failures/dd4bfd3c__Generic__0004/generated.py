import re
from typing import Dict

# Simulated database and CSRF token (would normally be stored securely)
database: Dict[int, dict] = {}
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token-123"

# Regular expression for a simple international phone number (digits, spaces, dashes, parentheses)
PHONE_REGEX = re.compile(r"^\+?[0-9\s\-\(\)]+$")


def update_user_phone(request: Dict) -> bool:
    """
    Update the phone number for a user in the simulated database.

    Parameters
    ----------
    request : dict
        Dictionary representing the HTTP request. It must contain:
            - headers: dict with a 'X-CSRF-Token' key.
            - body: dict containing:
                * 'user_id': int
                * 'new_phone_number': str

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.
    """
    # 1. CSRF token validation
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid CSRF token
        return False

    # 2. Extract body data
    body = request.get("body", {})
    user_id = body.get("user_id")
    new_phone_number = body.get("new_phone_number")

    # 3. Basic input validation
    if not isinstance(user_id, int):
        return False

    if not isinstance(new_phone_number, str) or not PHONE_REGEX.match(new_phone_number):
        return False

    # 4. Check if user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 5. Update the phone number
    try:
        user_record["phone_number"] = new_phone_number
        # In a real application, persist the change to the database here.
    except Exception:
        return False

    return True