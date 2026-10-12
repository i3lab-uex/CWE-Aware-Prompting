import re
from typing import Dict

# Sample user database (in a real application this would be a persistent store)
database: Dict[int, Dict[str, str]] = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"},
}

# Preconfigured CSRF token
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_123"

# Regular expression for a simple international phone number format
PHONE_REGEX = re.compile(r"^\+?[1-9]\d{1,14}$")


def alter_user_phone(service_request: Dict) -> bool:
    """
    Update a user's phone number in the database.

    Parameters
    ----------
    service_request : dict
        Expected keys:
            - headers: dict, must contain 'X-CSRF-Token'
            - body   : dict, must contain 'user_id' (int) and 'new_phone' (str)

    Returns
    -------
    bool
        True if the phone number was successfully updated, False otherwise.
    """
    try:
        # 1. Validate CSRF token
        headers = service_request.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            return False

        # 2. Extract body parameters
        body = service_request.get("body", {})
        user_id = body.get("user_id")
        new_phone = body.get("new_phone")

        if not isinstance(user_id, int) or not isinstance(new_phone, str):
            return False

        # 3. Validate phone number format
        if not PHONE_REGEX.match(new_phone):
            return False

        # 4. Update database
        user_record = database.get(user_id)
        if not user_record:
            return False

        user_record["phone"] = new_phone
        return True

    except Exception:
        # In case of unexpected errors, do not expose details
        return False