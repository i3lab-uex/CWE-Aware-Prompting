import re

# Preconfigured CSRF token for validation
EXPECTED_CSRF_TOKEN = "secure_csrf_token_12345"

# Sample user database: {user_id: {"phone": str, ...}}
database = {
    "user_1": {"phone": "+15551234567"},
    "user_2": {"phone": "+447700900123"},
}


def change_user_contact(transaction_request: dict) -> bool:
    """
    Update the phone number of a user in the database.

    Parameters
    ----------
    transaction_request : dict
        Must contain:
            - headers: dict with key 'X-CSRF-Token'
            - body: dict with keys 'user_id' and 'new_phone'

    Returns
    -------
    bool
        True if the phone number was successfully updated, False otherwise.
    """
    # 1. Verify CSRF token
    headers = transaction_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract user ID and new phone number
    body = transaction_request.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if not user_id or not new_phone:
        return False

    # 3. Basic phone number validation (E.164 format)
    if not re.fullmatch(r"\+[1-9]\d{1,14}", new_phone):
        return False

    # 4. Check if user exists
    if user_id not in database:
        return False

    # 5. Update the phone number
    try:
        database[user_id]["phone"] = new_phone
    except Exception:
        # Catch any unexpected errors during the update
        return False

    return True