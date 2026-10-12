import re

# Simulated database: user_id -> dict with user info
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"},
}

# Expected CSRF token for this example
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

# Regular expression for basic international phone number validation
PHONE_REGEX = re.compile(r"^\+?[1-9]\d{1,14}$")  # E.164 format

def update_user_phone(request: dict) -> bool:
    """
    Update a user's phone number in the simulated database.

    Parameters
    ----------
    request : dict
        Expected to contain:
            - 'headers': dict, may include 'X-CSRF-Token'
            - 'body': dict, must contain 'user_id' (int) and 'new_phone' (str)

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.
    """
    # 1. Verify CSRF token
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract and validate request body
    body = request.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    # Basic type checks
    if not isinstance(user_id, int) or not isinstance(new_phone, str):
        return False

    # 3. Validate phone number format
    if not PHONE_REGEX.match(new_phone):
        return False

    # 4. Check that the user exists
    user = database.get(user_id)
    if user is None:
        return False

    # 5. Update the phone number
    user["phone"] = new_phone
    return True