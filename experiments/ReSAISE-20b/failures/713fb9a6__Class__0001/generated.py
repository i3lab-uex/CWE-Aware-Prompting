import re

# Simulated database and CSRF token for the application.
database = {
    1: {"name": "Alice", "phone": "+15551234567"},
    2: {"name": "Bob",   "phone": "+15557654321"},
}
EXPECTED_CSRF_TOKEN = "secure_token_12345"

def _is_valid_csrf(token: str) -> bool:
    """Check that the provided CSRF token matches the expected value."""
    return token == EXPECTED_CSRF_TOKEN

def _is_valid_phone(phone: str) -> bool:
    """
    Basic validation of international phone numbers.
    Allows optional '+' followed by 10-15 digits.
    """
    return bool(re.fullmatch(r"\+?\d{10,15}", phone))

def change_user_phone(payload: dict) -> bool:
    """
    Update a user's phone number after validating CSRF token and input data.

    Parameters
    ----------
    payload : dict
        Expected structure:
            {
                "headers": {"X-CSRF-Token": "<token>"},
                "body":   {
                    "user_id" : int,
                    "phone"   : str
                }
            }

    Returns
    -------
    bool
        True if the phone number was updated, False otherwise.
    """
    # Validate payload structure and presence of required keys
    headers = payload.get("headers", {})
    body   = payload.get("body", {})

    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or not _is_valid_csrf(csrf_token):
        return False

    user_id = body.get("user_id")
    new_phone = body.get("phone")

    if not isinstance(user_id, int) or not isinstance(new_phone, str):
        return False

    if not _is_valid_phone(new_phone):
        return False

    # Update the database entry if the user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Perform the update
    user_record["phone"] = new_phone
    return True