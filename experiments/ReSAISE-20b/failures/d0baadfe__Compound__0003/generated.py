import re
from typing import Dict

# Sample user database: user_id -> phone number
database: Dict[str, str] = {
    "user123": "+1-555-1234",
    "alice": "+44 20 7946 0958"
}

# Preconfigured CSRF token
EXPECTED_CSRF_TOKEN: str = "s3cr3t-csrf-token"

# Regular expression to validate a phone number (very permissive)
PHONE_REGEX = re.compile(r"^\+?\d[\d\s\-()]{7,}\d$")


def _validate_csrf(headers: Dict[str, str]) -> bool:
    """
    Validate the CSRF token from request headers.
    The token is expected in the 'X-CSRF-Token' header.
    """
    token = headers.get("X-CSRF-Token")
    return token == EXPECTED_CSRF_TOKEN


def _validate_user_id(user_id: str) -> bool:
    """
    Basic validation to ensure the user ID exists in the database.
    """
    return user_id in database


def _validate_phone_number(phone: str) -> bool:
    """
    Validate the phone number format using a regex.
    """
    return bool(PHONE_REGEX.match(phone.strip()))


def modify_user_phone(user_request: Dict) -> bool:
    """
    Modify the phone number of a user.

    Parameters
    ----------
    user_request : dict
        A dictionary containing 'headers' and 'body'. The body must include:
        - 'user_id': str
        - 'new_phone': str

    Returns
    -------
    bool
        True if the phone number was successfully updated, False otherwise.
    """
    # 1. Extract headers and body
    headers = user_request.get("headers", {})
    body = user_request.get("body", {})

    # 2. CSRF protection
    if not _validate_csrf(headers):
        return False

    # 3. Extract required fields
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if not user_id or not new_phone:
        return False

    # 4. Validate user ID and phone number format
    if not _validate_user_id(user_id):
        return False

    if not _validate_phone_number(new_phone):
        return False

    # 5. Update the database
    try:
        database[user_id] = new_phone.strip()
    except Exception:
        return False

    # 6. Successful update
    return True