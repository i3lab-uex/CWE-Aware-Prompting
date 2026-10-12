import re

# Constants used by the function
EXPECTED_CSRF_TOKEN = "12345-abcde-67890-fghij"
# Simulated user database
database = {
    1: {"name": "Alice", "phone": "+15551234567"},
    2: {"name": "Bob",   "phone": "+15559876543"},
}

def _is_valid_phone(phone: str) -> bool:
    """
    Validate that the phone number consists of optional '+' followed by
    10 to 15 digits. This is a simple check; real-world validation would be more
    robust.
    """
    return bool(re.fullmatch(r"\+?\d{10,15}", phone))

def modify_user_phone(request_data: dict) -> bool:
    """
    Update the phone number of a user in the simulated database.

    Parameters
    ----------
    request_data : dict
        Dictionary containing:
            - headers: dict with 'X-CSRF-Token'
            - body:   dict with 'user_id' (int) and 'phone' (str)

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.
    """
    # 1. CSRF token validation
    headers = request_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body parameters
    body = request_data.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("phone")

    # 3. Basic type and existence checks
    if not isinstance(user_id, int) or user_id not in database:
        return False

    if not isinstance(new_phone, str) or not _is_valid_phone(new_phone):
        return False

    # 4. Update the database entry
    try:
        database[user_id]["phone"] = new_phone
        return True
    except Exception:  # pragma: no cover - defensive programming
        return False

# Example usage (uncomment to test)
# request = {
#     "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
#     "body": {"user_id": 1, "phone": "+15551230000"}
# }
# print(modify_user_phone(request))  # Should output: True