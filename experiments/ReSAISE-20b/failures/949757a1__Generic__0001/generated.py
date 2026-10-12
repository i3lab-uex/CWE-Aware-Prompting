import re

# Sample user database: key = user id (int), value = dict with user data
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"},
}

# Preconfigured CSRF token used for validation
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

# Regular expression for a simple international phone number format
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")


def change_user_contact(transaction_request: dict) -> bool:
    """
    Update a user's phone number in the `database`.

    Parameters
    ----------
    transaction_request : dict
        Must contain:
            - headers: dict with key 'X-CSRF-Token'
            - body   : dict with keys 'user_id' and 'new_phone'

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.
    """
    # --- Validate request structure -----------------------------------------
    if not isinstance(transaction_request, dict):
        return False

    headers = transaction_request.get("headers")
    body = transaction_request.get("body")

    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # --- CSRF protection ----------------------------------------------------
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # --- Extract user id and new phone --------------------------------------
    try:
        user_id = int(body["user_id"])
        new_phone = str(body["new_phone"]).strip()
    except (KeyError, ValueError, TypeError):
        return False

    # --- Validate phone number format --------------------------------------
    if not PHONE_REGEX.match(new_phone):
        return False

    # --- Update database ----------------------------------------------------
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Perform the update
    user_record["phone"] = new_phone
    return True


# Example usage (for testing purposes only)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body":   {"user_id": 1, "new_phone": "+15551234567"},
    }
    print(change_user_contact(request))  # Should output: True
    print(database[1]["phone"])          # Should show the updated phone number