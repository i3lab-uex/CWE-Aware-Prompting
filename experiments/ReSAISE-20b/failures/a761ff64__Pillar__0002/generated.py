import re

# Global configuration (simulated)
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

# Simulated in‑memory user database
# Structure: {user_id: {"phone": "+1234567890", ...}}
database = {
    1: {"phone": "+1111111111"},
    2: {"phone": "+2222222222"},
}


def _validate_csrf(headers: dict) -> bool:
    """
    Validate the CSRF token provided in request headers.
    """
    return headers.get("X-CSRF-Token") == EXPECTED_CSRF_TOKEN


def _validate_phone(phone: str) -> bool:
    """
    Basic validation of a phone number.
    Accepts E.164 format: + followed by 10-15 digits.
    """
    return bool(re.fullmatch(r"\+\d{10,15}", phone))


def alter_user_phone(input: dict) -> bool:
    """
    Update a user's phone number in the simulated database.

    Parameters
    ----------
    input : dict
        Expected keys:
            headers: dict containing 'X-CSRF-Token'
            body   : dict containing 'user_id' (int) and 'new_phone' (str)

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    # 1. CSRF validation
    headers = input.get("headers", {})
    if not _validate_csrf(headers):
        return False

    # 2. Extract body data
    body = input.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    # 3. Basic type checks
    if not isinstance(user_id, int) or not isinstance(new_phone, str):
        return False

    # 4. Phone format validation
    if not _validate_phone(new_phone):
        return False

    # 5. Update the database entry if user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 6. Perform the update
    try:
        user_record["phone"] = new_phone
    except Exception:
        return False

    return True