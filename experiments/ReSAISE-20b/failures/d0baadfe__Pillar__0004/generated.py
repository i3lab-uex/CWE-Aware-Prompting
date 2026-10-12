import re
from typing import Dict

# Sample database and CSRF token for demonstration purposes
database: Dict[int, dict] = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"},
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

# Regular expression for a basic E.164 phone number validation
PHONE_REGEX = re.compile(r"^\+?[1-9]\d{1,14}$")


def modify_user_phone(user_request: Dict) -> bool:
    """
    Update a user's phone number in the database.

    Parameters
    ----------
    user_request : dict
        Dictionary containing HTTP request data. Expected keys:
            - "headers": dict, must include a "X-CSRF-Token" header
            - "body":   dict, must contain:
                * "user_id"  : int
                * "new_phone": str

    Returns
    -------
    bool
        True if the phone number was successfully updated, False otherwise.
    """
    # 1. Validate CSRF token
    headers = user_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body parameters
    body = user_request.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_phone = body["new_phone"]
    except (KeyError, ValueError, TypeError):
        return False

    # 3. Validate phone number format
    if not isinstance(new_phone, str) or not PHONE_REGEX.fullmatch(new_phone):
        return False

    # 4. Update the database atomically (simulate transaction)
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Simple protection: make a shallow copy to avoid accidental mutation
    updated_record = user_record.copy()
    updated_record["phone"] = new_phone

    # Commit the change
    database[user_id] = updated_record
    return True