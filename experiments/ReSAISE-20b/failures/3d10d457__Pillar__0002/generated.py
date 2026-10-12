import re

# Mock database and constants (these would normally be defined elsewhere)
database = {
    # user_id: { 'phone': '1234567890', ... }
}
EXPECTED_CSRF_TOKEN = "expected_csrf_token_value"

def alter_user_phone(incoming_request: dict) -> bool:
    """
    Update a user's phone number in the mock database after validating CSRF token
    and ensuring the user exists. Returns True on success, False otherwise.
    """
    # 1. Extract CSRF token from headers
    headers = incoming_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid CSRF token
        return False

    # 2. Extract body parameters
    body = incoming_request.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    # 3. Basic validation of inputs
    if not user_id or not new_phone:
        return False

    # 4. Validate phone number format (simple regex: digits only, length 10-15)
    if not re.fullmatch(r"\d{10,15}", new_phone):
        return False

    # 5. Check that the user exists in the database
    if user_id not in database:
        return False

    # 6. Perform the update
    try:
        database[user_id]["phone"] = new_phone
    except Exception:
        # Any unexpected error should result in failure
        return False

    return True