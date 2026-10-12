import re

# Simulated database: user_id -> dict with 'phone' and other fields
database = {
    1: {"name": "Alice", "phone": "+15551234567"},
    2: {"name": "Bob",   "phone": "+15557654321"},
}

# Expected CSRF token for validation
EXPECTED_CSRF_TOKEN = "expected_csrf_token_value"

# Regular expression to validate phone numbers (simple E.164 format)
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")


def alter_user_phone(input: dict) -> bool:
    """
    Update a user's phone number after validating the CSRF token and input data.

    Parameters
    ----------
    input : dict
        Expected structure:
            {
                "headers": {"X-CSRF-Token": "<token>"},
                "body":    {
                    "user_id": <int>,
                    "phone"  : "<new phone number>"
                }
            }

    Returns
    -------
    bool
        True if the phone was updated successfully, False otherwise.
    """
    # 1. Validate CSRF token
    try:
        csrf_token = input["headers"]["X-CSRF-Token"]
    except (KeyError, TypeError):
        return False

    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Validate body structure
    try:
        body = input["body"]
        user_id = int(body["user_id"])
        new_phone = str(body["phone"]).strip()
    except (KeyError, TypeError, ValueError):
        return False

    # 3. Validate phone format
    if not PHONE_REGEX.match(new_phone):
        return False

    # 4. Update the database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Perform the update
    try:
        user_record["phone"] = new_phone
    except Exception:
        return False

    return True


# Example usage (for testing purposes)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "phone": "+15559876543"}
    }
    print(alter_user_phone(request))  # Should output: True
    print(database[1]["phone"])       # Should show the updated phone number