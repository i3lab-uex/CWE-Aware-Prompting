import re
from typing import Dict

# Mock database: key=user_id, value=dict with user details including 'phone'
database: Dict[int, Dict[str, str]] = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"},
}

# Expected CSRF token for verification
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

# Regular expression to validate international phone numbers (basic)
PHONE_REGEX = re.compile(r"^\+?[1-9]\d{1,14}$")


def alter_user_phone(incoming_request: Dict) -> bool:
    """
    Update a user's phone number after verifying CSRF token and input validity.

    Parameters
    ----------
    incoming_request : dict
        Dictionary containing request headers and body. Expected keys:
            - "headers": dict with a "X-CSRF-Token" header.
            - "body": dict with keys "user_id" (int) and "new_phone" (str).

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.
    """
    # 1. Verify CSRF token
    headers = incoming_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body data
    body = incoming_request.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_phone = str(body["new_phone"]).strip()
    except (KeyError, ValueError, TypeError):
        return False

    # 3. Validate phone number format
    if not PHONE_REGEX.match(new_phone):
        return False

    # 4. Check that the user exists in the database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 5. Update the phone number
    user_record["phone"] = new_phone
    return True

# Example usage (for testing purposes only)
if __name__ == "__main__":
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_phone": "+15551234567"}
    }
    success = alter_user_phone(req)
    print(f"Update successful: {success}")
    print(database[1])