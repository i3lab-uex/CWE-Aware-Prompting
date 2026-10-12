import re
from typing import Dict

# Simulated user database: {user_id: {"phone": "123-456-7890", ...}}
database: Dict[str, dict] = {}

# Expected CSRF token for validation
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token-123"

# Regular expression for validating phone numbers (simple US format)
PHONE_REGEX = re.compile(r"^\+?1?\s*\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$")


def modify_user_phone(request_data: Dict) -> bool:
    """
    Update a user's phone number after validating CSRF token and input.

    Args:
        request_data (dict): Dictionary containing
            - headers: {'X-CSRF-Token': str}
            - body:   {'user_id': str, 'new_phone': str}

    Returns:
        bool: True if the phone number was updated successfully, False otherwise.

    Raises:
        ValueError: If required fields are missing or invalid.
    """
    try:
        # Validate CSRF token
        csrf_token = request_data.get("headers", {}).get("X-CSRF-Token")
        if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
            return False

        body = request_data.get("body", {})
        user_id = body.get("user_id")
        new_phone = body.get("new_phone")

        if not user_id or not new_phone:
            return False

        # Validate phone number format
        if not PHONE_REGEX.match(new_phone):
            return False

        # Update the database entry if user exists
        user_record = database.get(user_id)
        if not user_record:
            return False

        # Perform the update
        user_record["phone"] = new_phone
        return True

    except Exception:
        # Log exception details in a real application; for now just swallow and return False
        return False

# Example usage (for testing purposes only):
if __name__ == "__main__":
    # Populate database with a test user
    database["user123"] = {"phone": "555-0100"}

    # Construct a valid request
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": "user123", "new_phone": "+1 (555) 123-4567"}
    }

    print(modify_user_phone(req))           # Expected: True
    print(database["user123"]["phone"])     # Expected updated phone number