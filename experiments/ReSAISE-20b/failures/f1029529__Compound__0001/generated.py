import re

# Mock database and expected CSRF token (for demonstration purposes)
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"},
}
EXPECTED_CSRF_TOKEN = "s3cUrEt0k3n"

# Regular expression for a simple international phone number format
PHONE_REGEX = re.compile(r"^\+?[1-9]\d{7,14}$")  # + followed by 8–15 digits


def modify_user_phone(client_request: dict) -> bool:
    """
    Update a user's phone number in the mock database.

    Parameters
    ----------
    client_request : dict
        Expected keys:
            - headers: dict containing 'X-CSRF-Token'
            - body: dict containing 'user_id' (int) and 'new_phone' (str)

    Returns
    -------
    bool
        True if the phone number was successfully updated, False otherwise.
    """

    # 1. Validate CSRF token
    headers = client_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body data
    body = client_request.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    # 3. Validate input types
    if not isinstance(user_id, int) or not isinstance(new_phone, str):
        return False

    # 4. Validate phone number format
    if not PHONE_REGEX.match(new_phone):
        return False

    # 5. Check that the user exists
    if user_id not in database:
        return False

    # 6. Perform the update
    try:
        database[user_id]["phone"] = new_phone
        return True
    except Exception:
        # In a real application you would log the exception
        return False