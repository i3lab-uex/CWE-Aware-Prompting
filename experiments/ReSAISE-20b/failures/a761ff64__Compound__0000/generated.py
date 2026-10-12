import re

# Pre‑defined CSRF token used by the application
EXPECTED_CSRF_TOKEN = "s3cr3t-csrf-token"

# Simulated user database: {user_id: {"phone": str, ...}}
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"},
}

# Regular expression to validate international phone numbers
PHONE_REGEX = re.compile(r"^\+?[1-9]\d{1,14}$")  # E.164 format


def alter_user_phone(input: dict) -> bool:
    """
    Update a user's phone number in the simulated database.

    Parameters
    ----------
    input : dict
        Request dictionary containing:
            - headers: {'X-CSRF-Token': str}
            - body:   {'user_id': int, 'new_phone': str}

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.

    Raises
    ------
    ValueError
        If required fields are missing or invalid.
    """

    # --- 1. CSRF token validation ------------------------------------
    headers = input.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid or missing CSRF token – reject the request
        return False

    # --- 2. Extract and validate input data --------------------------
    body = input.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_phone = str(body["new_phone"]).strip()
    except (KeyError, ValueError, TypeError):
        return False

    # Basic phone number format check (E.164)
    if not PHONE_REGEX.match(new_phone):
        return False

    # --- 3. Perform the update ---------------------------------------
    user_record = database.get(user_id)
    if not user_record:
        # User does not exist
        return False

    # Update the phone number in a thread‑safe manner if needed.
    user_record["phone"] = new_phone
    return True


# Example usage (for testing purposes only)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": "s3cr3t-csrf-token"},
        "body": {"user_id": 1, "new_phone": "+15551234567"}
    }
    print(alter_user_phone(request))  # Expected: True
    print(database[1]["phone"])       # Expected: +15551234567