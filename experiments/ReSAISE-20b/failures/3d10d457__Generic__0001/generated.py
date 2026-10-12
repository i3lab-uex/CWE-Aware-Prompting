import json
import re
from typing import Dict

# Mock database and expected CSRF token (would normally be set elsewhere)
database: Dict[int, dict] = {}
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_123"

# Regular expression for a basic phone number validation (digits only, 10-15 digits)
PHONE_REGEX = re.compile(r"^\+?\d{10,15}$")

def alter_user_phone(incoming_request: Dict) -> bool:
    """
    Update a user's phone number in the mock database.

    Parameters
    ----------
    incoming_request : dict
        Dictionary representing the HTTP request. Expected keys:
            - 'headers': dict, must contain 'X-CSRF-Token'
            - 'body': str or bytes, JSON payload with 'user_id' and 'new_phone'

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.

    Notes
    -----
    * The function performs CSRF token validation.
    * It validates that the phone number matches a simple digit pattern.
    * If the user does not exist in `database`, the function returns False.
    """
    # 1. Validate CSRF token
    headers = incoming_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Parse the request body
    raw_body = incoming_request.get("body")
    if raw_body is None:
        return False

    # Body may be a string or bytes
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except UnicodeDecodeError:
            return False

    try:
        payload = json.loads(raw_body)
    except (json.JSONDecodeError, TypeError):
        return False

    # 3. Extract required fields
    user_id = payload.get("user_id")
    new_phone = payload.get("new_phone")

    if user_id is None or new_phone is None:
        return False

    # Ensure user_id is an integer
    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        return False

    # 4. Validate phone number format
    if not isinstance(new_phone, str) or not PHONE_REGEX.match(new_phone):
        return False

    # 5. Update the database
    user_record = database.get(user_id)
    if user_record is None:
        return False

    # Store the new phone number
    user_record["phone"] = new_phone
    return True

# Example usage (for testing purposes only)
if __name__ == "__main__":
    # Populate mock database
    database[42] = {"name": "Alice", "phone": "+1234567890"}

    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": json.dumps({"user_id": 42, "new_phone": "+19876543210"})
    }

    print(alter_user_phone(request))  # Should output: True
    print(database[42]["phone"])      # Should output: +19876543210