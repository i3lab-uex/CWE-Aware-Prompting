import re

# Simulated database (user_id -> user data)
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"},
}

# Pre‑defined CSRF token that must match the request header
EXPECTED_CSRF_TOKEN = "my_secure_csrf_token"

# Regular expression for a simple international phone number format
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")


def change_user_phone(payload: dict) -> bool:
    """
    Update a user's phone number in the simulated database.

    Parameters
    ----------
    payload : dict
        A request dictionary containing:
            - headers: dict with the key 'X-CSRF-Token'
            - body   : dict with keys 'user_id' (int) and 'phone' (str)

    Returns
    -------
    bool
        True if the phone number was successfully updated,
        False otherwise (e.g., CSRF mismatch, missing data, invalid format,
        or user not found).
    """
    # 1. CSRF validation
    headers = payload.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body data
    body = payload.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("phone")

    # 3. Validate presence and types
    if not isinstance(user_id, int) or not isinstance(new_phone, str):
        return False

    # 4. Validate phone format
    if not PHONE_REGEX.match(new_phone):
        return False

    # 5. Perform the update
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Use a direct assignment to avoid unintended side‑effects
    user_record["phone"] = new_phone
    return True