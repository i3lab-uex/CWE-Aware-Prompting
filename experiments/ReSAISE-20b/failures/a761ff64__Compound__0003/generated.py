import re

# Simulated global data (would normally be provided by the framework)
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+0987654321"}
}
EXPECTED_CSRF_TOKEN = "secure_token_123"

# Regular expression for a simple international phone number validation
PHONE_REGEX = re.compile(r"^\+?[0-9]{7,15}$")

def alter_user_phone(input: dict) -> bool:
    """
    Update the phone number of a user after validating CSRF token and input.

    Parameters
    ----------
    input : dict
        Expected structure:
            {
                "headers": {"X-CSRF-Token": "<token>"},
                "body":    {
                                "user_id": <int>,
                                "new_phone": "<string>"
                            }
            }

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    # 1. Validate CSRF token
    try:
        token = input["headers"]["X-CSRF-Token"]
    except (KeyError, TypeError):
        return False
    if token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Validate body structure
    try:
        user_id = input["body"]["user_id"]
        new_phone = input["body"]["new_phone"]
    except (KeyError, TypeError):
        return False

    # 3. Validate user_id type
    if not isinstance(user_id, int):
        return False

    # 4. Validate phone number format
    if not isinstance(new_phone, str) or not PHONE_REGEX.match(new_phone):
        return False

    # 5. Perform the update
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 6. Update the phone number
    user_record["phone"] = new_phone
    return True