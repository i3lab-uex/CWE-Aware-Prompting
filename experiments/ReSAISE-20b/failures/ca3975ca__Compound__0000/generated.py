import re

# Predefined CSRF token that must match the request header
EXPECTED_CSRF_TOKEN = "a1b2c3d4e5f6g7h8"

# Simulated user database: {user_id (int): {"phone": str, ...}}
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"},
}


def modify_user_phone(request_data: dict) -> bool:
    """
    Update a user's phone number after validating CSRF token and input data.

    Parameters
    ----------
    request_data : dict
        A dictionary containing:
            - 'headers': dict with a 'X-CSRF-Token' key
            - 'body':   dict with keys:
                - 'user_id' : int or str convertible to int
                - 'phone'   : new phone number string

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.

    Notes
    -----
    * The CSRF token must match `EXPECTED_CSRF_TOKEN`.
    * The phone number is validated to be a string of 10–15 digits,
      optionally prefixed with '+' and spaces are removed.
    * The function is defensive against missing keys, wrong types,
      or non-existent users.

    Security
    --------
    This implementation mitigates CWE-352 (CSRF) by requiring a matching CSRF token.
    Input validation prevents injection of malicious data into the database.
    """

    # 1. Validate presence of required top‑level keys
    if not isinstance(request_data, dict):
        return False

    headers = request_data.get("headers")
    body = request_data.get("body")

    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # 2. CSRF token validation
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 3. Extract and validate user ID
    raw_user_id = body.get("user_id")
    try:
        user_id = int(raw_user_id)
    except (TypeError, ValueError):
        return False

    # 4. Extract and validate new phone number
    raw_phone = body.get("phone")
    if not isinstance(raw_phone, str):
        return False

    # Normalize: remove spaces and dashes
    phone = re.sub(r"[\s\-]", "", raw_phone)

    # Basic format check: optional '+' followed by 10-15 digits
    if not re.fullmatch(r"\+?\d{10,15}", phone):
        return False

    # 5. Update the database if user exists
    user_record = database.get(user_id)
    if user_record is None:
        return False

    # Perform the update
    user_record["phone"] = phone
    return True


# Example usage (for testing purposes only)
if __name__ == "__main__":
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "phone": "+1555 1234567"},
    }
    print(modify_user_phone(req))          # Expected: True
    print(database[1]["phone"])            # Expected: +15551234567