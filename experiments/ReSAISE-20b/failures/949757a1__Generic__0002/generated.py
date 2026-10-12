import re
from typing import Dict, Any

# Sample user database: mapping user_id -> dict with 'phone' field
database: Dict[str, Dict[str, Any]] = {
    "user1": {"phone": "+1234567890"},
    "user2": {"phone": "+0987654321"},
}

# Preconfigured CSRF token for validation
EXPECTED_CSRF_TOKEN: str = "s3cr3tCsRfT0ken"


def _is_valid_phone(phone: str) -> bool:
    """
    Basic validation for international phone numbers.
    Accepts digits, spaces, dashes, parentheses and leading +.
    """
    pattern = re.compile(r"^\+?[0-9\s\-\(\)]+$")
    return bool(pattern.match(phone))


def change_user_contact(transaction_request: Dict[str, Any]) -> bool:
    """
    Update a user's phone number in the database.

    Parameters
    ----------
    transaction_request : dict
        Expected structure:
            {
                "headers": {"X-CSRF-Token": "<token>", ...},
                "body": {
                    "user_id": "<string>",
                    "new_phone": "<string>"
                }
            }

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    # Validate presence of required keys
    headers = transaction_request.get("headers")
    body = transaction_request.get("body")

    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # CSRF token validation
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # Extract user ID and new phone number
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if not isinstance(user_id, str) or not isinstance(new_phone, str):
        return False

    # Basic phone number validation
    if not _is_valid_phone(new_phone):
        return False

    # Check that the user exists
    user_record = database.get(user_id)
    if user_record is None:
        return False

    # Update the phone number
    try:
        user_record["phone"] = new_phone
    except Exception:
        return False

    return True