import re
from typing import Dict

# Sample in‑memory database of users: {user_id: {"phone": str, ...}}
database: Dict[int, dict] = {
    1: {"name": "Alice", "phone": "+15551234567"},
    2: {"name": "Bob",   "phone": "+15557654321"},
}

# Preconfigured CSRF token that the server expects to receive
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_123"

# Regular expression for a basic international phone number (e.g., +15551234567)
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")


def modify_user_phone(user_request: Dict) -> bool:
    """
    Update a user's phone number in the global `database`.

    Parameters
    ----------
    user_request : dict
        Expected structure:
            {
                "headers": {"X-CSRF-Token": "<token>"},
                "body":   {
                    "user_id" : <int>,
                    "phone"   : "<+1234567890>"
                }
            }

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.

    Notes
    -----
    * CSRF protection is validated against EXPECTED_CSRF_TOKEN.
    * Input validation ensures that `user_id` is an integer and `phone`
      matches a simple international format.
    * The function performs no external I/O; it only mutates the in‑memory
      `database` dictionary.
    """
    # 1. Validate CSRF token
    headers = user_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not isinstance(csrf_token, str) or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body and validate presence of required keys
    body = user_request.get("body", {})
    if not isinstance(body, dict):
        return False

    # 3. Validate user_id
    user_id_raw = body.get("user_id")
    try:
        user_id = int(user_id_raw)
    except (TypeError, ValueError):
        return False

    # 4. Validate phone number format
    phone_raw = body.get("phone")
    if not isinstance(phone_raw, str) or not PHONE_REGEX.fullmatch(phone_raw):
        return False

    # 5. Update database if user exists
    user_record = database.get(user_id)
    if not isinstance(user_record, dict):
        return False

    # Perform the update
    user_record["phone"] = phone_raw
    return True


# Example usage (for testing purposes only; remove in production)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body":   {"user_id": 1, "phone": "+15559876543"}
    }
    result = modify_user_phone(request)
    print("Update succeeded:", result)          # Expected: True
    print("New phone:", database[1]["phone"])   # Expected: +15559876543