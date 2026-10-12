import re

# Simulated database: user_id -> dict of user info
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"},
}

# Expected CSRF token for validation
EXPECTED_CSRF_TOKEN = "s3cr3t-csrf-token"

# Regular expression for a simple E.164 phone number format
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")

def update_user_phone(request: dict) -> bool:
    """
    Update the phone number of a user.

    Parameters
    ----------
    request : dict
        Dictionary containing:
            - headers: dict, should contain 'X-CSRF-Token'
            - body: dict, should contain:
                * 'user_id': int
                * 'new_phone': str

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.
    """
    # 1. CSRF token validation
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract and validate payload
    body = request.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if not isinstance(user_id, int) or user_id <= 0:
        return False
    if not isinstance(new_phone, str) or not PHONE_REGEX.match(new_phone):
        return False

    # 3. Verify user exists
    if user_id not in database:
        return False

    # 4. Update phone number
    database[user_id]["phone"] = new_phone
    return True

# Example usage:
if __name__ == "__main__":
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body":    {"user_id": 1, "new_phone": "+15551234567"}
    }
    print(update_user_phone(req))  # Should print: True