import re

# Simulated user database: {user_id: {"phone": "...", ...}}
database = {}

# Predefined CSRF token for validation
EXPECTED_CSRF_TOKEN = "secure_token_123"

def alter_user_phone(input: dict) -> bool:
    """
    Update a user's phone number in the simulated database.

    Parameters
    ----------
    input : dict
        Request dictionary containing:
            - headers: {"csrf_token": str}
            - body: {"user_id": int, "new_phone": str}

    Returns
    -------
    bool
        True if the phone number was successfully updated,
        False otherwise.
    """
    # Validate CSRF token
    headers = input.get("headers", {})
    csrf_token = headers.get("csrf_token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # Extract body fields
    body = input.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    # Basic validation of inputs
    if not isinstance(user_id, int) or not isinstance(new_phone, str):
        return False

    # Phone number format check: 10-15 digits, optionally with + prefix
    phone_pattern = re.compile(r"^\+?\d{10,15}$")
    if not phone_pattern.match(new_phone):
        return False

    # Ensure user exists in the database
    if user_id not in database:
        return False

    # Update phone number securely (replace the entire field)
    try:
        database[user_id]["phone"] = new_phone
        return True
    except Exception:
        # Catch any unexpected errors during update
        return False