import re

# Predefined CSRF token that the server expects.
EXPECTED_CSRF_TOKEN = "secure_csrf_token_12345"

# Simulated user database.
# Example structure: {user_id: {"phone": "123-456-7890", ...}}
database = {
    1: {"name": "Alice", "phone": "555-0100"},
    2: {"name": "Bob",   "phone": "555-0200"}
}

# Regular expression for a simple phone number validation
PHONE_REGEX = re.compile(r"^\+?\d{1,3}?[-.\s]??\(?\d{1,4}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}$")


def alter_user_phone(input: dict) -> bool:
    """
    Update a user's phone number after verifying CSRF token and input validity.

    Args:
        input (dict): Request dictionary containing headers and body.
            Expected format:
                {
                    "headers": {"X-CSRF-Token": "<token>"},
                    "body": {"user_id": <int>, "new_phone": "<str>"}
                }

    Returns:
        bool: True if the update succeeded, False otherwise.
    """
    # 1. CSRF token validation
    try:
        csrf_token = input["headers"]["X-CSRF-Token"]
    except (KeyError, TypeError):
        # Missing token or headers structure
        return False

    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid CSRF token
        return False

    # 2. Extract body parameters
    try:
        user_id = input["body"]["user_id"]
        new_phone = input["body"]["new_phone"]
    except (KeyError, TypeError):
        # Missing body or required fields
        return False

    # 3. Validate user_id type
    if not isinstance(user_id, int):
        return False

    # 4. Validate phone number format
    if not isinstance(new_phone, str) or not PHONE_REGEX.match(new_phone):
        return False

    # 5. Perform the update in the simulated database
    user_record = database.get(user_id)
    if not user_record:
        # User does not exist
        return False

    # Update the phone number
    user_record["phone"] = new_phone
    return True


# Example usage (uncomment to test):
# request = {
#     "headers": {"X-CSRF-Token": "secure_csrf_token_12345"},
#     "body": {"user_id": 1, "new_phone": "+1 (555) 123-4567"}
# }
# print(alter_user_phone(request))   # Should output: True