import re
from typing import Dict

# Sample user database (user_id -> dict with phone)
database: Dict[str, Dict] = {
    "u123": {"phone": "+15551234567"},
    "u456": {"phone": "+15557654321"},
}

# Preconfigured CSRF token
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

# Regex pattern for international phone numbers (basic validation)
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")


def modify_user_phone(user_request: Dict) -> bool:
    """
    Update the phone number for a user in the database.

    Parameters
    ----------
    user_request : dict
        Dictionary containing headers and a body. The body must include:
            - "user_id": str
            - "new_phone": str

    Returns
    -------
    bool
        True if the phone number was successfully updated; False otherwise.
    """
    # 1. Validate CSRF token
    headers = user_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token") or headers.get("csrf-token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body data
    body = user_request.get("body")
    if not isinstance(body, dict):
        return False

    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if not user_id or not isinstance(user_id, str):
        return False
    if not new_phone or not isinstance(new_phone, str):
        return False

    # 3. Validate phone number format
    if not PHONE_REGEX.match(new_phone):
        return False

    # 4. Update the database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # In a real application, we would also ensure that the new phone
    # number is unique and not already used by another user.
    user_record["phone"] = new_phone
    return True