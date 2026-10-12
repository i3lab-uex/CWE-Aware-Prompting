import re
from typing import Dict

# Mock database and expected CSRF token (normally these would be configured elsewhere)
database: Dict[int, Dict[str, str]] = {}
EXPECTED_CSRF_TOKEN: str = "secure-token-123"

# Regular expression for a simple international phone number validation
PHONE_REGEX = re.compile(r"^\+?[1-9]\d{1,14}$")  # E.164 format


def change_user_phone(request_details: Dict) -> bool:
    """
    Update a user's phone number after verifying CSRF token and input validity.

    Parameters
    ----------
    request_details : dict
        Dictionary containing at least:
            - 'headers': a mapping of header names to values.
            - 'body': a mapping with keys 'user_id' and 'new_phone'.

    Returns
    -------
    bool
        True if the phone number was updated successfully; False otherwise.
    """
    try:
        headers = request_details["headers"]
        body = request_details["body"]

        # 1. CSRF token verification
        csrf_token = headers.get("X-CSRF-Token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            return False

        # 2. Extract and validate user ID
        user_id = body.get("user_id")
        if not isinstance(user_id, int):
            return False
        if user_id not in database:
            return False

        # 3. Validate new phone number
        new_phone = body.get("new_phone")
        if not isinstance(new_phone, str):
            return False
        if not PHONE_REGEX.match(new_phone):
            return False

        # 4. Perform the update
        database[user_id]["phone"] = new_phone
        return True

    except (KeyError, TypeError):
        # Malformed request structure
        return False