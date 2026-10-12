import re
from typing import Dict

# Simulated database and expected CSRF token
database: Dict[int, dict] = {
    1: {"name": "Alice", "phone": "555-1234"},
    2: {"name": "Bob",   "phone": "555-5678"},
}
EXPECTED_CSRF_TOKEN = "secure_token_123"

# Regular expression for a simple phone number validation
PHONE_REGEX = re.compile(r"^\+?[0-9\s\-]{7,15}$")


def update_user_phone(request: Dict) -> bool:
    """
    Update a user's phone number after verifying CSRF token and input validity.

    Args:
        request (dict): Request object containing headers and body.
            Expected structure:
                {
                    "headers": {"X-CSRF-Token": "..."},
                    "body": {"user_id": <int>, "new_phone": "<string>"}
                }

    Returns:
        bool: True if the phone number was updated successfully, False otherwise.
    """
    # 1. Validate CSRF token
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body data
    body = request.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    # 3. Basic validation of input types
    if not isinstance(user_id, int) or not isinstance(new_phone, str):
        return False

    # 4. Validate phone number format
    if not PHONE_REGEX.match(new_phone):
        return False

    # 5. Check that the user exists in the database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 6. Update the phone number
    user_record["phone"] = new_phone.strip()
    return True


# Example usage (for testing purposes only)
if __name__ == "__main__":
    sample_request = {
        "headers": {"X-CSRF-Token": "secure_token_123"},
        "body": {"user_id": 1, "new_phone": "+1-800-555-0199"},
    }
    print(update_user_phone(sample_request))  # Expected: True
    print(database[1]["phone"])              # Expected: "+1-800-555-0199"