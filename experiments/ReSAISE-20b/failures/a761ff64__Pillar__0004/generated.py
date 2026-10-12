import hmac
from typing import Dict

# Simulated database of users: user_id -> dict with 'phone' field
database: Dict[int, Dict[str, str]] = {
    1: {"phone": "555-0100"},
    2: {"phone": "555-0200"},
}

# Expected CSRF token for validation
EXPECTED_CSRF_TOKEN = "super-secret-csrf-token"

def _validate_csrf(provided_token: str) -> bool:
    """
    Validate the CSRF token using a constant-time comparison to mitigate timing attacks.
    Returns True if tokens match, False otherwise.
    """
    return hmac.compare_digest(provided_token, EXPECTED_CSRF_TOKEN)

def alter_user_phone(input: Dict) -> bool:
    """
    Update the phone number of a user after validating CSRF token.

    Parameters
    ----------
    input : dict
        A request dictionary containing:
            - headers: dict with 'X-CSRF-Token' key
            - body: dict with 'user_id' (int) and 'new_phone' (str)

    Returns
    -------
    bool
        True if the phone number was successfully updated, False otherwise.
    """
    # 1. Validate CSRF token
    headers = input.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or not _validate_csrf(csrf_token):
        return False

    # 2. Extract user ID and new phone number
    body = input.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_phone = str(body["new_phone"]).strip()
    except (KeyError, ValueError):
        return False

    # 3. Validate phone number format (basic check: digits, dashes, spaces)
    if not new_phone or not all(c.isdigit() or c in "- " for c in new_phone):
        return False

    # 4. Update the database if user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Perform the update
    user_record["phone"] = new_phone
    return True