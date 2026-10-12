import re

# Mock database and CSRF token for demonstration purposes.
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"},
}
EXPECTED_CSRF_TOKEN = "secure_csrf_token_123"

# Regular expression for a simple international phone number validation.
PHONE_REGEX = re.compile(r"^\+\d{7,15}$")

def modify_user_phone(client_request: dict) -> bool:
    """
    Update a user's phone number in the mock database.

    Parameters
    ----------
    client_request : dict
        Dictionary representing an HTTP request. Expected keys:
            - "headers": dict containing at least "X-CSRF-Token".
            - "body": dict with keys:
                * "user_id" (int)
                * "new_phone" (str)

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.
    """
    try:
        # 1. Validate CSRF token
        headers = client_request.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            return False

        # 2. Extract body data
        body = client_request.get("body", {})
        user_id = body.get("user_id")
        new_phone = body.get("new_phone")

        # 3. Basic type checks
        if not isinstance(user_id, int) or not isinstance(new_phone, str):
            return False

        # 4. Validate phone format
        if not PHONE_REGEX.match(new_phone):
            return False

        # 5. Ensure user exists
        if user_id not in database:
            return False

        # 6. Update the phone number
        database[user_id]["phone"] = new_phone
        return True

    except Exception:
        # In a real application you would log the exception.
        return False