import re
from typing import Dict

# Simulated database and CSRF token for the example
database: Dict[int, Dict[str, str]] = {
    1: {"name": "Alice", "phone": "+15551234567"},
    2: {"name": "Bob",   "phone": "+15559876543"},
}
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_12345"

# Regular expression to validate international phone numbers (E.164 format)
PHONE_REGEX = re.compile(r"^\+?[1-9]\d{1,14}$")


def modify_user_phone(request_data: Dict) -> bool:
    """
    Update the phone number of a user in the simulated database.

    Parameters
    ----------
    request_data : dict
        Expected structure:
            {
                "headers": {"X-CSRF-Token": "<token>"},
                "body":   {
                    "user_id": <int>,
                    "new_phone": "<phone_number>"
                }
            }

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.

    Raises
    ------
    ValueError
        If required fields are missing or malformed.
    """
    # 1. Validate CSRF token
    try:
        csrf_token = request_data["headers"]["X-CSRF-Token"]
    except KeyError:
        # Missing token header
        return False

    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid CSRF token
        return False

    # 2. Extract body fields
    try:
        body = request_data["body"]
        user_id = int(body["user_id"])
        new_phone = body["new_phone"].strip()
    except (KeyError, ValueError, AttributeError):
        # Malformed request
        return False

    # 3. Validate phone number format
    if not PHONE_REGEX.match(new_phone):
        return False

    # 4. Update the database entry if user exists
    if user_id not in database:
        return False

    # Perform the update
    database[user_id]["phone"] = new_phone
    return True