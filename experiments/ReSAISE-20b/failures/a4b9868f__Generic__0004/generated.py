import re

# Sample user database (user_id -> user record)
database = {
    1: {"name": "Alice", "phone": "5551234567"},
    2: {"name": "Bob",   "phone": "5559876543"},
}

# Preconfigured CSRF token
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

def alter_user_phone(service_request: dict) -> bool:
    """
    Update the phone number of a user in the `database`.

    Parameters
    ----------
    service_request : dict
        Dictionary containing 'headers' and 'body'.  The body must contain
        the keys 'user_id' (int or str convertible to int) and
        'phone' (str of digits, 10–15 characters).

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    # 1. Validate CSRF token
    headers = service_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body fields
    body = service_request.get("body", {})
    if not isinstance(body, dict):
        return False

    user_id_raw = body.get("user_id")
    phone = body.get("phone")

    if user_id_raw is None or phone is None:
        return False

    # 3. Normalize and validate user_id
    try:
        user_id = int(user_id_raw)
    except (ValueError, TypeError):
        return False

    # 4. Validate phone number format
    if not isinstance(phone, str) or not re.fullmatch(r"\d{10,15}", phone):
        return False

    # 5. Perform the update
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Update phone number
    user_record["phone"] = phone
    return True