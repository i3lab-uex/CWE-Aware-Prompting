import re
from typing import Dict

# Mock database and CSRF token for demonstration purposes
database: Dict[int, Dict[str, str]] = {
    1: {"name": "Alice", "phone": "555-1234"},
    2: {"name": "Bob",   "phone": "555-5678"},
}
EXPECTED_CSRF_TOKEN = "secure-token-123"

# Regular expression for a simple phone number validation (e.g., 10 digits)
PHONE_REGEX = re.compile(r"^\+?\d{7,15}$")

def modify_user_phone(client_request: Dict) -> bool:
    """
    Update a user's phone number after verifying CSRF token and input validity.

    Parameters
    ----------
    client_request : dict
        Expected keys:
            - headers: dict, must contain 'X-CSRF-Token'
            - body: dict, must contain 'user_id' (int) and 'new_phone' (str)

    Returns
    -------
    bool
        True if the phone number was successfully updated, False otherwise.
    """
    try:
        # 1. CSRF token validation (CWE-693: protection mechanism failure)
        headers = client_request.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            return False  # token mismatch

        # 2. Extract and validate body parameters
        body = client_request.get("body", {})
        user_id = body.get("user_id")
        new_phone = body.get("new_phone")

        if not isinstance(user_id, int) or user_id <= 0:
            return False

        if not isinstance(new_phone, str) or not PHONE_REGEX.match(new_phone):
            return False

        # 3. Update the mock database
        user_record = database.get(user_id)
        if not user_record:
            return False

        # Simulate a secure update operation
        user_record["phone"] = new_phone
        return True

    except Exception:
        # Log the exception in a real application; here we simply fail gracefully
        return False

# Example usage:
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": "secure-token-123"},
        "body": {"user_id": 1, "new_phone": "+15551234567"},
    }
    print(modify_user_phone(request))  # Expected output: True