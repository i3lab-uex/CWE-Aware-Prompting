import re

# Sample user database (user_id -> dict)
database = {
    1: {"name": "Alice", "phone": "1234567890"},
    2: {"name": "Bob",   "phone": "0987654321"}
}

# Preconfigured CSRF token
EXPECTED_CSRF_TOKEN = "s3cr3t_t0k3n"

def change_user_contact(transaction_request: dict) -> bool:
    """
    Update the phone number of a user in the database.

    Parameters
    ----------
    transaction_request : dict
        Expected structure:
            {
                "headers": {"X-CSRF-Token": "..."},
                "body":   {"user_id": 1, "phone": "5551234567"}
            }

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    # 1. Validate CSRF token
    headers = transaction_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid or missing CSRF token
        return False

    # 2. Extract and validate body payload
    body = transaction_request.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("phone")

    # Ensure user_id is an integer and exists in the database
    if not isinstance(user_id, int) or user_id not in database:
        return False

    # Validate phone number: only digits, length 10-15 (adjust as needed)
    if not isinstance(new_phone, str) or not re.fullmatch(r"\d{10,15}", new_phone):
        return False

    # 3. Perform the update
    try:
        database[user_id]["phone"] = new_phone
    except Exception:
        # Any unexpected error results in failure
        return False

    return True