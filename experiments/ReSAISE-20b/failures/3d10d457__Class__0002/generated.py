import re

# Mock database and constants (in a real application these would be imported)
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"},
}
EXPECTED_CSRF_TOKEN = "secure-token-123"

def alter_user_phone(incoming_request: dict) -> bool:
    """
    Update a user's phone number in the mock database after validating
    CSRF token, user existence, and phone format.

    Parameters:
        incoming_request (dict): Dictionary containing headers and body.
            Expected keys:
                - 'headers': dict with a 'X-CSRF-Token' key.
                - 'body': dict with keys 'user_id' (int) and 'new_phone' (str).

    Returns:
        bool: True if the phone number was updated successfully, False otherwise.
    """
    # 1. Validate CSRF token
    headers = incoming_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body parameters
    body = incoming_request.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    # 3. Basic type and presence checks
    if not isinstance(user_id, int) or not isinstance(new_phone, str):
        return False

    # 4. Verify phone number format (simple E.164 validation)
    if not re.fullmatch(r"\+[1-9]\d{1,14}", new_phone):
        return False

    # 5. Check that the user exists in the database
    if user_id not in database:
        return False

    # 6. Update the phone number
    try:
        database[user_id]["phone"] = new_phone
    except Exception:
        return False

    # 7. Return success flag
    return True