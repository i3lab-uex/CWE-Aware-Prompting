import re
import hmac
from typing import Dict

# Mock database and CSRF token constant for demonstration purposes
database: Dict[int, Dict[str, str]] = {}
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_value"

# Regular expression for a basic phone number validation (e.g., 10-15 digits, optional +)
PHONE_REGEX = re.compile(r"^\+?\d{10,15}$")

def _is_valid_phone(phone: str) -> bool:
    """Validate the phone number format."""
    return bool(PHONE_REGEX.match(phone))

def change_user_phone(request_details: Dict) -> bool:
    """
    Update a user's phone number after verifying CSRF token and input validity.

    Args:
        request_details (dict): Dictionary containing 'headers' and 'body'.
            Expected keys in body: 'user_id', 'new_phone'.

    Returns:
        bool: True if update succeeded, False otherwise.
    """
    try:
        # Extract headers and body
        headers = request_details.get("headers", {})
        body = request_details.get("body", {})

        # Verify CSRF token using constant‑time comparison
        csrf_token = headers.get("X-CSRF-Token", "")
        if not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
            return False

        # Retrieve and validate user ID
        user_id_raw = body.get("user_id")
        if user_id_raw is None:
            return False
        try:
            user_id = int(user_id_raw)
        except (TypeError, ValueError):
            return False

        # Retrieve and validate new phone number
        new_phone = body.get("new_phone")
        if not isinstance(new_phone, str) or not _is_valid_phone(new_phone):
            return False

        # Check that the user exists in the mock database
        if user_id not in database:
            return False

        # Perform the update
        database[user_id]["phone"] = new_phone
        return True

    except Exception:
        # In production, log the exception; here we simply return False
        return False

# Example usage (for testing purposes only):
if __name__ == "__main__":
    # Populate mock database
    database[1] = {"name": "Alice", "phone": "+1234567890"}
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_phone": "+19876543210"}
    }
    result = change_user_phone(request)
    print("Update succeeded:", result)  # Expected: True
    print("Updated record:", database[1])