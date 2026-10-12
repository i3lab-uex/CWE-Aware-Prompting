import re
from typing import Dict

# Simulated user database: {user_id: {"phone": str, ...}}
database: Dict[int, dict] = {}

# Predefined CSRF token for the application
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_12345"

# Regular expression to validate phone numbers (simple E.164 format)
PHONE_REGEX = re.compile(r"^\+?[1-9]\d{1,14}$")


def alter_user_phone(input: Dict) -> bool:
    """
    Update the phone number of a user after validating CSRF token and input.

    Parameters
    ----------
    input : dict
        A request dictionary containing:
            - headers: dict with 'X-CSRF-Token'
            - body: dict with 'user_id' (int) and 'new_phone' (str)

    Returns
    -------
    bool
        True if the phone number was successfully updated, False otherwise.
    """
    try:
        # Extract CSRF token
        csrf_token = input.get("headers", {}).get("X-CSRF-Token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            # Invalid CSRF token
            return False

        # Extract body data
        body = input.get("body", {})
        user_id = body.get("user_id")
        new_phone = body.get("new_phone")

        # Basic validation of input types
        if not isinstance(user_id, int) or not isinstance(new_phone, str):
            return False

        # Validate phone format
        if not PHONE_REGEX.match(new_phone):
            return False

        # Check user exists in the database
        if user_id not in database:
            return False

        # Perform the update atomically (simulated)
        database[user_id]["phone"] = new_phone
        return True

    except Exception:
        # Any unexpected error should result in failure without leaking details
        return False


# Example usage (for testing purposes only)
if __name__ == "__main__":
    # Populate the database with a sample user
    database[1] = {"name": "Alice", "phone": "+1234567890"}

    # Prepare a valid request
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_phone": "+19876543210"},
    }

    success = alter_user_phone(req)
    print("Update succeeded:", success)          # Expected: True
    print("New phone:", database[1]["phone"])     # Expected: +19876543210