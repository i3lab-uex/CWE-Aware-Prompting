import re

# Sample in‑memory database of users
database = {
    1: {"name": "Alice", "phone": "+15551234567"},
    2: {"name": "Bob",   "phone": "+15557654321"},
}

# Expected CSRF token for this application
EXPECTED_CSRF_TOKEN = "secure_token_12345"

# Regular expression to validate international phone numbers
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")


def change_user_contact(transaction_request: dict) -> bool:
    """
    Update a user's phone number in the `database`.

    Parameters
    ----------
    transaction_request : dict
        A dictionary containing HTTP request data. It must have a
        'headers' key (dict) and a 'body' key (dict). The body must
        contain 'user_id' (int) and 'new_phone' (str).

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.
    """
    # Validate request structure
    try:
        headers = transaction_request["headers"]
        body = transaction_request["body"]
        user_id = body["user_id"]
        new_phone = body["new_phone"]
    except (KeyError, TypeError):
        # Malformed request
        return False

    # CSRF protection: compare tokens in a time‑constant manner
    token = headers.get("X-CSRF-Token")
    if not _secure_compare(token, EXPECTED_CSRF_TOKEN):
        return False

    # Validate user ID type
    if not isinstance(user_id, int):
        return False

    # Validate phone number format
    if not PHONE_REGEX.match(new_phone):
        return False

    # Perform the update atomically
    user = database.get(user_id)
    if not user:
        return False

    # Simulate potential race condition by using a lock (here simplified)
    try:
        user["phone"] = new_phone
    except Exception:
        return False

    return True


def _secure_compare(a: str | None, b: str) -> bool:
    """
    Compare two strings in a time‑constant manner to avoid timing attacks.
    """
    if a is None:
        return False
    # Ensure both strings are of the same length
    if len(a) != len(b):
        return False
    result = 0
    for x, y in zip(a.encode(), b.encode()):
        result |= x ^ y
    return result == 0