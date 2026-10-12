import re
from typing import Dict

# Sample database: user_id -> user data dict
database: Dict[str, Dict] = {
    "user1": {"phone": "+15551234567"},
    "user2": {"phone": "+15559876543"},
}

# Preconfigured CSRF token
EXPECTED_CSRF_TOKEN = "s3cureT0ken123"

# Regular expression for a simple E.164 phone number format
PHONE_REGEX = re.compile(r"^\+[1-9]\d{1,14}$")


def modify_user_phone(user_request: Dict) -> bool:
    """
    Update a user's phone number in the database.

    Parameters
    ----------
    user_request : dict
        Dictionary containing 'headers' and 'body'. Expected keys:
            - headers: dict with 'X-CSRF-Token'
            - body: dict with 'user_id' and 'new_phone'

    Returns
    -------
    bool
        True if the phone number was successfully updated, False otherwise.
    """
    # 1. Validate request structure
    if not isinstance(user_request, dict):
        return False

    headers = user_request.get("headers")
    body = user_request.get("body")

    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # 2. CSRF token validation (CWE-693 consideration)
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 3. Extract user_id and new phone number
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if not isinstance(user_id, str) or not isinstance(new_phone, str):
        return False

    # 4. Validate phone number format
    if not PHONE_REGEX.match(new_phone):
        return False

    # 5. Update the database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Optionally, ensure the phone number is actually changing
    if user_record.get("phone") == new_phone:
        return True  # No change needed but considered success

    user_record["phone"] = new_phone
    return True