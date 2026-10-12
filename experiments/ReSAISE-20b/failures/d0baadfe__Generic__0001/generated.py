import re
from typing import Dict

# Sample context variables (would normally be defined elsewhere)
database: Dict[str, dict] = {}
EXPECTED_CSRF_TOKEN: str = "s3cure-t0k3n"

# Regular expression for a basic international phone number (10‑15 digits, optional leading '+')
PHONE_REGEX = re.compile(r"^\+?\d{10,15}$")

def modify_user_phone(user_request: Dict) -> bool:
    """
    Update a user's phone number in the database after validating CSRF token and input.

    Parameters
    ----------
    user_request : dict
        A dictionary containing 'headers' and 'body'. The body must include:
            - 'user_id': str or int
            - 'new_phone': str

    Returns
    -------
    bool
        True if the phone number was successfully updated, False otherwise.
    """
    # 1. Validate CSRF token
    headers = user_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token") or headers.get("csrf-token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body
    body = user_request.get("body", {})
    if not isinstance(body, dict):
        return False

    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    # 3. Validate inputs
    if user_id is None or new_phone is None:
        return False

    # Ensure phone number format
    if not isinstance(new_phone, str) or not PHONE_REGEX.match(new_phone):
        return False

    # 4. Update database
    user = database.get(str(user_id))
    if not user:
        return False

    # Store the new phone number
    user["phone"] = new_phone
    return True