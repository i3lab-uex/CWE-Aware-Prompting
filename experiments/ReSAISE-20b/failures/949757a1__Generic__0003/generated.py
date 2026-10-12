import re

# Preconfigured CSRF token
EXPECTED_CSRF_TOKEN = "S3cureT0k3n"

# Sample user database
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"},
}


def change_user_contact(transaction_request: dict) -> bool:
    """
    Update a user's phone number in the `database` based on the provided
    transaction request.

    Parameters
    ----------
    transaction_request : dict
        Dictionary containing HTTP-like headers and a body. Expected keys:
            - "headers": dict with key "X-CSRF-Token"
            - "body": dict with keys "user_id" (int) and "new_phone" (str)

    Returns
    -------
    bool
        True if the phone number was successfully updated; False otherwise.
    """
    # 1. Validate presence of headers and body
    headers = transaction_request.get("headers")
    body = transaction_request.get("body")

    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # 2. CSRF token validation
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 3. Extract user ID and new phone number
    try:
        user_id = int(body["user_id"])
        new_phone = body["new_phone"]
    except (KeyError, ValueError):
        return False

    # 4. Validate phone number format (simple E.164-ish check)
    if not isinstance(new_phone, str) or not re.fullmatch(r"\+?\d{7,15}", new_phone):
        return False

    # 5. Update database if user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    user_record["phone"] = new_phone
    return True