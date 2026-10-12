import re
from typing import Dict

# Mock database and expected CSRF token (these would normally be provided by the surrounding system)
database: Dict[int, Dict[str, str]] = {
    1: {"name": "Alice", "phone": "+15551234567"},
    2: {"name": "Bob",   "phone": "+15559876543"},
}
EXPECTED_CSRF_TOKEN: str = "secure-token-123"

# Regular expression for a simple international phone number validation
PHONE_REGEX = re.compile(r"^\+?[1-9]\d{1,14}$")  # E.164 format


def alter_user_phone(incoming_request: Dict) -> bool:
    """
    Update a user's phone number in the mock database.

    Parameters
    ----------
    incoming_request : dict
        Expected to contain a 'headers' dict with the CSRF token and a 'body'
        dict containing 'user_id' (int) and 'new_phone' (str).

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.
    """
    # 1. Validate CSRF token
    headers = incoming_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body data
    body = incoming_request.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    # 3. Basic type checks
    if not isinstance(user_id, int) or not isinstance(new_phone, str):
        return False

    # 4. Validate phone number format
    if not PHONE_REGEX.match(new_phone):
        return False

    # 5. Update the database entry if user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 6. Perform the update
    user_record["phone"] = new_phone
    return True