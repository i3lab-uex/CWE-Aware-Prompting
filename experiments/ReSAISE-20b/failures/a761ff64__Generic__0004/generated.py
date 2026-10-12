import re
from typing import Dict

# Global constants and database placeholder
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token-123"
database: Dict[int, dict] = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob", "phone": "+1987654321"},
}

def _validate_csrf(headers: Dict[str, str]) -> bool:
    """
    Validate the CSRF token present in request headers.
    """
    return headers.get("X-CSRF-Token") == EXPECTED_CSRF_TOKEN

def _validate_phone_number(phone: str) -> bool:
    """
    Basic phone number validation.
    Accepts international format with optional +, digits only,
    length between 10 and 15 characters.
    """
    pattern = re.compile(r"^\+?\d{10,15}$")
    return bool(pattern.match(phone))

def alter_user_phone(input: Dict) -> bool:
    """
    Update the phone number of a user in the simulated database.

    Parameters
    ----------
    input : dict
        Request dictionary containing:
            - headers: dict with CSRF token under key "X-CSRF-Token"
            - body: dict with keys:
                * user_id (int)
                * new_phone (str)

    Returns
    -------
    bool
        True if the phone number was updated successfully,
        False otherwise.

    Raises
    ------
    ValueError
        If required fields are missing or invalid.
    """
    # 1. Validate CSRF token
    headers = input.get("headers", {})
    if not _validate_csrf(headers):
        return False

    # 2. Extract body parameters
    body = input.get("body")
    if not isinstance(body, dict):
        return False

    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if user_id is None or new_phone is None:
        return False

    # 3. Validate phone number format
    if not _validate_phone_number(new_phone):
        return False

    # 4. Check that user exists
    if not isinstance(user_id, int) or user_id not in database:
        return False

    # 5. Update the phone number
    try:
        database[user_id]["phone"] = new_phone
    except Exception:
        return False

    return True

# Example usage (for testing purposes only)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_phone": "+15551234567"},
    }
    print(alter_user_phone(request))  # Expected: True
    print(database[1]["phone"])       # Expected: +15551234567