import re

# Simulated global database and CSRF token
database = {}  # Example: {1: {"phone": "123-456-7890"}, ...}
EXPECTED_CSRF_TOKEN = "secure-csrf-token"

def _is_valid_phone(phone: str) -> bool:
    """
    Basic phone number validation.
    Accepts digits, spaces, dashes, parentheses and plus sign.
    """
    pattern = re.compile(r"^\+?[\d\s\-\(\)]{7,20}$")
    return bool(pattern.match(phone))

def change_user_phone(payload: dict) -> bool:
    """
    Update the phone number of a user.

    Parameters
    ----------
    payload : dict
        Request dictionary containing:
            - headers: dict with 'X-CSRF-Token'
            - body   : dict with 'user_id' (int) and 'new_phone' (str)

    Returns
    -------
    bool
        True if the update succeeds, False otherwise.
    """
    # 1. Validate CSRF token
    headers = payload.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body data
    body = payload.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    # 3. Basic type checks
    if not isinstance(user_id, int) or not isinstance(new_phone, str):
        return False

    # 4. Validate phone format
    if not _is_valid_phone(new_phone):
        return False

    # 5. Update database entry if user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 6. Perform the update
    try:
        user_record["phone"] = new_phone
        return True
    except Exception:
        # In case the user record is immutable or other unexpected error
        return False

# Example usage (for testing only):
if __name__ == "__main__":
    # Setup a sample user
    database[42] = {"phone": "555-1234"}
    payload_valid = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 42, "new_phone": "+1 (555) 987-6543"}
    }
    print(change_user_phone(payload_valid))          # Should output: True
    print(database[42]["phone"])                    # Updated phone number