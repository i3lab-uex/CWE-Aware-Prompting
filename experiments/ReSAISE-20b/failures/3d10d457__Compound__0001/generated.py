import re
from typing import Dict

# Mock database: user_id -> dict with phone number
database: Dict[str, Dict[str, str]] = {
    "user1": {"phone": "+1234567890"},
    "user2": {"phone": "+0987654321"},
}

# Expected CSRF token for the application
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token-1234"


def _validate_csrf_token(headers: Dict[str, str]) -> bool:
    """
    Validate the CSRF token present in request headers.
    The token is expected to be under the key 'X-CSRF-Token'.
    """
    token = headers.get("X-CSRF-Token", "")
    return token == EXPECTED_CSRF_TOKEN


def _validate_phone_number(phone: str) -> bool:
    """
    Very simple phone number validation.
    Accepts digits, optional leading '+', and length between 7 and 15 characters.
    """
    pattern = re.compile(r"^\+?\d{7,15}$")
    return bool(pattern.match(phone))


def alter_user_phone(incoming_request: Dict) -> bool:
    """
    Update a user's phone number in the mock database.

    Parameters
    ----------
    incoming_request : dict
        Dictionary containing request headers and body.
        Expected structure:
            {
                "headers": {"X-CSRF-Token": "<token>", ...},
                "body":   {"user_id": "<id>", "new_phone": "<number>"}
            }

    Returns
    -------
    bool
        True if the phone number was updated successfully,
        False otherwise (e.g., CSRF token missing/invalid, user not found,
        or phone number format invalid).
    """
    # 1. CSRF protection
    headers = incoming_request.get("headers", {})
    if not _validate_csrf_token(headers):
        return False

    # 2. Extract body data
    body = incoming_request.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    # 3. Basic input validation
    if not isinstance(user_id, str) or not isinstance(new_phone, str):
        return False

    if not _validate_phone_number(new_phone):
        return False

    # 4. Update the mock database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Update phone number
    user_record["phone"] = new_phone
    return True