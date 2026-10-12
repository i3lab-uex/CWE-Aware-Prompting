import re

# Mock database and CSRF token for demonstration purposes
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"},
}
EXPECTED_CSRF_TOKEN = "secure-token-123"

# Regular expression for a simple international phone number validation
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")

def alter_user_phone(incoming_request: dict) -> bool:
    """
    Update a user's phone number in the mock database after validating
    CSRF token, user existence, and phone format.

    Parameters:
        incoming_request (dict): Should contain 'headers' with a
            'X-CSRF-Token' key and a 'body' dict containing:
                - 'user_id': int
                - 'new_phone': str

    Returns:
        bool: True if update succeeded, False otherwise.
    """
    # 1. Verify CSRF token
    headers = incoming_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body and validate its structure
    body = incoming_request.get("body")
    if not isinstance(body, dict):
        return False

    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if not isinstance(user_id, int) or not isinstance(new_phone, str):
        return False

    # 3. Validate phone number format
    if not PHONE_REGEX.match(new_phone):
        return False

    # 4. Check user existence in the database
    if user_id not in database:
        return False

    # 5. Perform the update
    try:
        database[user_id]["phone"] = new_phone
    except Exception:
        return False

    return True