import re
import hmac
from typing import Dict, Any

# Mock database: user_id -> dict of user attributes
database: Dict[str, Dict[str, Any]] = {
    "user123": {"phone": "+15551234567"},
    # other users...
}

# Expected CSRF token value
EXPECTED_CSRF_TOKEN = "secure_expected_token_value"

def _validate_csrf(token: str) -> bool:
    """
    Compare CSRF tokens using constant‑time comparison to mitigate timing attacks.
    """
    return hmac.compare_digest(token, EXPECTED_CSRF_TOKEN)

def _validate_phone_number(phone: str) -> bool:
    """
    Basic validation of international phone numbers.
    Accepts + followed by 10–15 digits.
    """
    return bool(re.fullmatch(r"\+\d{10,15}", phone))

def alter_user_phone(incoming_request: Dict[str, Any]) -> bool:
    """
    Update a user's phone number in the mock database.

    Args:
        incoming_request: dict containing headers and body with user_id and new_phone.

    Returns:
        bool: True if update succeeded, False otherwise.
    """
    try:
        # Extract CSRF token from headers
        csrf_token = incoming_request.get("headers", {}).get("X-CSRF-Token")
        if not csrf_token or not _validate_csrf(csrf_token):
            return False

        # Extract body data
        body = incoming_request.get("body", {})
        user_id = str(body.get("user_id"))
        new_phone = body.get("new_phone")

        if not user_id or not new_phone:
            return False

        # Validate phone format
        if not _validate_phone_number(new_phone):
            return False

        # Ensure user exists in the database
        if user_id not in database:
            return False

        # Perform the update
        database[user_id]["phone"] = new_phone
        return True

    except Exception:
        # Log exception in real application; suppress to avoid leaking info
        return False