import re
from typing import Dict

# Mock database and CSRF token
database: Dict[int, dict] = {
    1: {"name": "Alice", "phone": "+15551234567"},
    2: {"name": "Bob",   "phone": "+15557654321"},
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

# Regular expression for a simple international phone number validation
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")


def change_user_phone(request_details: Dict) -> bool:
    """
    Update a user's phone number in the mock database.

    Parameters
    ----------
    request_details : dict
        Must contain:
            headers: dict, with key "X-CSRF-Token" holding the CSRF token.
            body   : dict, with keys "user_id" (int) and "new_phone" (str).

    Returns
    -------
    bool
        True if the phone number was updated, False otherwise.

    Raises
    ------
    ValueError
        If required fields are missing or malformed.
    """
    # 1. Validate CSRF token
    headers = request_details.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body
    body = request_details.get("body")
    if not isinstance(body, dict):
        return False

    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if not isinstance(user_id, int) or not isinstance(new_phone, str):
        return False

    # 3. Validate phone number format
    if not PHONE_REGEX.match(new_phone):
        return False

    # 4. Update the database atomically
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Simple lock simulation (no actual concurrency control needed for this mock)
    user_record["phone"] = new_phone
    return True