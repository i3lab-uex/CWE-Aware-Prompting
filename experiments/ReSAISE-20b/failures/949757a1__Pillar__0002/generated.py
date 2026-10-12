import re

# Sample user database: {user_id: {"phone": "...", ...}}
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"}
}

# Expected CSRF token (in a real app this would be securely stored)
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

# Regular expression for a simple international phone number validation
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")


def change_user_contact(transaction_request: dict) -> bool:
    """
    Update the phone number of a user in the database.

    Parameters
    ----------
    transaction_request : dict
        Expected structure:
            {
                "headers": {"X-CSRF-Token": "..."},
                "body":   {"user_id": int, "new_phone": str}
            }

    Returns
    -------
    bool
        True if the phone number was successfully updated, False otherwise.
    """
    # 1. Validate request structure
    if not isinstance(transaction_request, dict):
        return False

    headers = transaction_request.get("headers")
    body = transaction_request.get("body")

    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # 2. CSRF protection (CWE-693 consideration)
    csrf_token = headers.get("X-CSRF-Token")
    if not isinstance(csrf_token, str) or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 3. Extract and validate user ID
    user_id = body.get("user_id")
    if not isinstance(user_id, int):
        return False

    # 4. Extract and validate new phone number
    new_phone = body.get("new_phone")
    if not isinstance(new_phone, str) or not PHONE_REGEX.match(new_phone):
        return False

    # 5. Perform the update if user exists
    user_record = database.get(user_id)
    if user_record is None:
        return False

    # Update the phone number
    user_record["phone"] = new_phone
    return True