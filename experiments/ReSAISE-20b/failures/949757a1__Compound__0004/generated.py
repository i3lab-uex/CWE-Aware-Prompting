import re
from typing import Dict

# Sample database and CSRF token (normally these would be defined elsewhere)
database: Dict[int, Dict[str, str]] = {}
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_123"

# Regular expression for a basic phone number validation (digits, +, spaces, dashes)
PHONE_REGEX = re.compile(r"^\+?[0-9\s\-]{7,20}$")


def change_user_contact(transaction_request: Dict) -> bool:
    """
    Update a user's phone number in the database after verifying CSRF token
    and validating input data.

    Parameters
    ----------
    transaction_request : dict
        Must contain:
            - 'headers': dict with a key 'X-CSRF-Token'
            - 'body': dict containing:
                * 'user_id' : int
                * 'new_phone' : str

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.
    """
    # 1. Basic structure checks
    if not isinstance(transaction_request, dict):
        return False

    headers = transaction_request.get("headers")
    body = transaction_request.get("body")

    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # 2. CSRF token validation
    csrf_token = headers.get("X-CSRF-Token")
    if not isinstance(csrf_token, str) or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 3. Extract and validate user ID
    user_id = body.get("user_id")
    if not isinstance(user_id, int):
        return False

    # 4. Extract and validate new phone number
    new_phone = body.get("new_phone")
    if not isinstance(new_phone, str) or not PHONE_REGEX.match(new_phone):
        return False

    # 5. Update the database if user exists
    user_record = database.get(user_id)
    if not isinstance(user_record, dict):
        return False

    # Update the phone number
    user_record["phone"] = new_phone.strip()
    return True

# Example usage (for testing purposes only)
if __name__ == "__main__":
    # Populate sample database
    database[42] = {"phone": "555-1234"}

    # Create a valid request
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 42, "new_phone": "+1-800-555-0199"},
    }

    result = change_user_contact(req)
    print("Update succeeded:", result)          # Expected: True
    print("New phone:", database[42]["phone"])  # Expected: +1-800-555-0199