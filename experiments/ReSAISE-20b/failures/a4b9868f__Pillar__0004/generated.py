import re
from typing import Dict

# Sample database and CSRF token (in a real app these would be secure)
database: Dict[int, Dict[str, str]] = {
    1: {"name": "Alice", "phone": "123-456-7890"},
    2: {"name": "Bob",   "phone": "987-654-3210"},
}
EXPECTED_CSRF_TOKEN = "secure_token_123"

# Regular expression to validate phone numbers (simple E.164 or common formats)
PHONE_REGEX = re.compile(r"^\+?\d{10,15}$")


def alter_user_phone(service_request: Dict) -> bool:
    """
    Update a user's phone number after validating the CSRF token and input format.

    Parameters
    ----------
    service_request : dict
        Dictionary containing 'headers' and 'body'.
        Expected keys:
            - headers['X-CSRF-Token'] : CSRF token string
            - body['user_id']        : int user ID
            - body['new_phone']      : str new phone number

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    try:
        # 1. Validate CSRF token
        headers = service_request.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            return False

        # 2. Extract and validate body data
        body = service_request.get("body", {})
        user_id = body.get("user_id")
        new_phone = body.get("new_phone")

        if not isinstance(user_id, int) or user_id <= 0:
            return False

        if not isinstance(new_phone, str) or not PHONE_REGEX.match(new_phone):
            return False

        # 3. Update the database
        user_record = database.get(user_id)
        if not user_record:
            return False

        # Perform the update
        user_record["phone"] = new_phone
        return True

    except Exception:
        # In production, log the exception but do not expose details
        return False