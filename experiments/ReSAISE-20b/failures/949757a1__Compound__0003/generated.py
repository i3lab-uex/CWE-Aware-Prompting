import re

# Sample user database (user_id -> dict with phone)
database = {
    "user123": {"phone": "+15551234567"},
    "user456": {"phone": "+15557654321"},
}

# Preconfigured CSRF token that must be matched
EXPECTED_CSRF_TOKEN = "secure_csrf_token_12345"

# Regular expression to validate international phone numbers (basic)
PHONE_REGEX = re.compile(r"^\+?\d{10,15}$")


def change_user_contact(transaction_request: dict) -> bool:
    """
    Update a user's phone number after validating the CSRF token and
    ensuring the new phone number is well-formed.

    Parameters
    ----------
    transaction_request : dict
        Expected to contain:
            - 'headers': dict, may include 'X-CSRF-Token'
            - 'body': dict with keys 'user_id' and 'new_phone'

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.
    """
    # 1. CSRF token validation
    headers = transaction_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body data
    body = transaction_request.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if not user_id or not new_phone:
        return False

    # 3. Validate phone number format
    if not PHONE_REGEX.match(new_phone):
        return False

    # 4. Check that the user exists
    if user_id not in database:
        return False

    # 5. Update the phone number
    try:
        database[user_id]["phone"] = new_phone
        return True
    except Exception:
        # Any unexpected error should not expose internals
        return False