import re
from typing import Dict

# Simulated database and CSRF token (would normally be stored securely)
database: Dict[int, dict] = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"}
}
EXPECTED_CSRF_TOKEN = "s3cr3t-csrf-token"

# Regular expression for a simple international phone number (e.g., +1234567890)
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")


def modify_user_phone(request_data: Dict) -> bool:
    """
    Update a user's phone number after verifying CSRF token and validating input.

    Args:
        request_data (dict): Contains 'headers' with 'X-CSRF-Token'
                             and 'body' with 'user_id' (int) and 'new_phone' (str).

    Returns:
        bool: True if the update succeeded, False otherwise.

    Raises:
        ValueError: If required fields are missing or invalid.
    """
    # 1. Validate CSRF token
    headers = request_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF token mismatch: reject the request
        return False

    # 2. Extract and validate body data
    body = request_data.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if user_id is None or new_phone is None:
        return False

    # Ensure user_id is an integer
    if not isinstance(user_id, int):
        return False

    # Validate phone number format
    if not PHONE_REGEX.match(new_phone):
        return False

    # 3. Update the database entry if user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Perform the update
    user_record["phone"] = new_phone
    return True


# Example usage (for testing purposes only):
if __name__ == "__main__":
    req = {
        "headers": {"X-CSRF-Token": "s3cr3t-csrf-token"},
        "body": {"user_id": 1, "new_phone": "+11234567890"}
    }
    print(modify_user_phone(req))  # Should output: True
    print(database[1]["phone"])   # Should show the updated number