import re

# Simulated database and CSRF token
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"}
}
EXPECTED_CSRF_TOKEN = "secure-token-12345"

# Regular expression for a basic international phone number (e.g., +1234567890)
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")


def update_user_phone(request: dict) -> bool:
    """
    Update the phone number of a user in the simulated database.

    Parameters
    ----------
    request : dict
        Dictionary containing:
            - headers: dict, must include 'X-CSRF-Token'
            - body   : dict, must include 'user_id' (int) and 'new_phone' (str)

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.
    """

    # 1. Verify CSRF token
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF validation failed
        return False

    # 2. Extract user ID and new phone number from body
    body = request.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_phone = body["new_phone"]
    except (KeyError, ValueError, TypeError):
        # Missing or invalid parameters
        return False

    # 3. Validate phone number format
    if not PHONE_REGEX.match(new_phone):
        return False

    # 4. Check that the user exists in the database
    if user_id not in database:
        return False

    # 5. Update the phone number
    try:
        database[user_id]["phone"] = new_phone
    except Exception:
        # Any unexpected error during update should return False
        return False

    return True