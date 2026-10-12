import re
from typing import Dict

# Mock database: user_id -> dict with phone and other info
database: Dict[int, Dict[str, str]] = {
    1: {"name": "Alice", "phone": "+15551234567"},
    2: {"name": "Bob",   "phone": "+15559876543"},
}

# Expected CSRF token for validation
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

# Regular expression for a simple E.164 phone number validation
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")

def modify_user_phone(client_request: Dict) -> bool:
    """
    Update a user's phone number in the mock database.

    Parameters
    ----------
    client_request : dict
        Dictionary containing request headers and body. Expected keys:
            - 'headers': dict with 'X-CSRF-Token'
            - 'body'   : dict with 'user_id' (int) and 'new_phone' (str)

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.
    """
    # 1. CSRF token validation
    headers = client_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body data
    body = client_request.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    # 3. Basic input validation
    if not isinstance(user_id, int) or not isinstance(new_phone, str):
        return False

    # 4. Phone number format check
    if not PHONE_REGEX.match(new_phone):
        return False

    # 5. Check user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 6. Update phone number
    try:
        user_record["phone"] = new_phone
        return True
    except Exception:
        # In a real system we would log the exception
        return False

# Example usage (for demonstration; remove or comment out in production)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_phone": "+15551230000"},
    }
    success = modify_user_phone(request)
    print("Update succeeded:", success)
    print("Updated record:", database[1])