import re

# Pre‑defined CSRF token that must match the request header.
EXPECTED_CSRF_TOKEN = "secure_token_12345"

# Simulated user database: {user_id (int): {"phone": str, ...}}
database = {
    1: {"name": "Alice", "phone": "+15551234567"},
    2: {"name": "Bob",   "phone": "+15557654321"},
}


def _validate_csrf(request_headers: dict) -> bool:
    """
    Validate the CSRF token present in request headers.
    """
    token = request_headers.get("X-CSRF-Token") or request_headers.get("csrf-token")
    return token == EXPECTED_CSRF_TOKEN


def _validate_phone_number(phone: str) -> bool:
    """
    Basic validation for E.164 phone number format.
    Accepts '+' followed by 10-15 digits.
    """
    pattern = re.compile(r"^\+\d{10,15}$")
    return bool(pattern.match(phone))


def alter_user_phone(input: dict) -> bool:
    """
    Update a user's phone number in the simulated database.

    Parameters
    ----------
    input : dict
        Expected to contain:
            headers: dict with CSRF token
            body   : dict with keys 'user_id' (int) and 'phone' (str)

    Returns
    -------
    bool
        True if the phone number was updated, False otherwise.
    """
    # 1. CSRF protection
    headers = input.get("headers", {})
    if not _validate_csrf(headers):
        return False

    # 2. Extract body
    body = input.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("phone")

    # 3. Basic type and presence checks
    if not isinstance(user_id, int) or not isinstance(new_phone, str):
        return False

    # 4. Phone number format validation
    if not _validate_phone_number(new_phone):
        return False

    # 5. Update database if user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 6. Perform the update
    user_record["phone"] = new_phone
    return True


# Example usage (for demonstration only, not part of the module)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "phone": "+15559876543"},
    }
    print(alter_user_phone(request))  # Expected: True