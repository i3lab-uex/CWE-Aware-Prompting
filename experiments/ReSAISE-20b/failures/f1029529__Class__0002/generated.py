import re

# Constants and mock database
EXPECTED_CSRF_TOKEN = "expected_csrf_token_12345"
database = {
    1: {"name": "Alice", "phone": "+15551234567"},
    2: {"name": "Bob",   "phone": "+15559876543"},
}

# Regular expression for a simple international phone number format
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")


def modify_user_phone(client_request: dict) -> bool:
    """
    Update a user's phone number in the mock database.

    Parameters
    ----------
    client_request : dict
        Expected structure:
            {
                "headers": {"X-CSRF-Token": "..."},
                "body":   {"user_id": int, "new_phone": str}
            }

    Returns
    -------
    bool
        True if the update succeeds, False otherwise.
    """

    # 1. Verify CSRF token
    headers = client_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body data
    body = client_request.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    # 3. Basic validation of input types
    if not isinstance(user_id, int) or not isinstance(new_phone, str):
        return False

    # 4. Validate phone number format
    if not PHONE_REGEX.match(new_phone):
        return False

    # 5. Check user existence
    if user_id not in database:
        return False

    # 6. Perform the update
    try:
        database[user_id]["phone"] = new_phone
        return True
    except Exception:
        # Any unexpected error during update should result in failure
        return False