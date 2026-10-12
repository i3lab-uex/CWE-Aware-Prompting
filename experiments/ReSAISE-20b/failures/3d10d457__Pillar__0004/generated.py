import re
from typing import Dict

# Mock database and expected CSRF token
database: Dict[int, Dict[str, str]] = {}
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_value"

# Regular expression for a simple phone number validation
PHONE_REGEX = re.compile(r"^\+?[0-9]{7,15}$")


def alter_user_phone(incoming_request: Dict) -> bool:
    """
    Update a user's phone number after validating CSRF token and input data.

    Parameters
    ----------
    incoming_request : dict
        Dictionary containing at least:
            - headers: dict with a 'X-CSRF-Token' key
            - body: dict with keys:
                * 'user_id': int or str convertible to int
                * 'new_phone': str

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.
    """
    try:
        # 1. Validate CSRF token
        headers = incoming_request.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            # Invalid or missing CSRF token
            return False

        # 2. Extract and validate user ID
        body = incoming_request.get("body", {})
        user_id_raw = body.get("user_id")
        if user_id_raw is None:
            return False
        try:
            user_id = int(user_id_raw)
        except (TypeError, ValueError):
            return False

        # 3. Validate new phone number format
        new_phone = body.get("new_phone")
        if not isinstance(new_phone, str) or not PHONE_REGEX.match(new_phone):
            return False

        # 4. Ensure the user exists in the database
        if user_id not in database:
            return False

        # 5. Update the phone number
        database[user_id]["phone"] = new_phone
        return True

    except Exception:
        # Catch any unforeseen errors to avoid leaking information
        return False


# Example usage (for testing purposes only)
if __name__ == "__main__":
    # Populate mock database
    database[1] = {"phone": "+1234567890", "name": "Alice"}
    request_success = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_phone": "+19876543210"}
    }
    request_fail = {
        "headers": {"X-CSRF-Token": "wrong_token"},
        "body": {"user_id": 1, "new_phone": "+19876543210"}
    }

    print(alter_user_phone(request_success))  # Expected: True
    print(alter_user_phone(request_fail))     # Expected: False