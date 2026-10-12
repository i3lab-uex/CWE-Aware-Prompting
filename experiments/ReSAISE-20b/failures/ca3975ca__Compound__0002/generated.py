import re
from typing import Dict

# Simulated user database (user_id -> dict of attributes)
database: Dict[str, Dict] = {}

# Pre‑defined CSRF token that must match the request header
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token-1234"

# Regular expression for a simple international phone number validation
PHONE_REGEX = re.compile(r"^\+?[1-9]\d{1,14}$")


def modify_user_phone(request_data: Dict) -> bool:
    """
    Update the phone number of a user in the simulated database.

    Parameters
    ----------
    request_data : dict
        A dictionary with two keys:
            - 'headers': a mapping containing the CSRF token under key 'X-CSRF-Token'
            - 'body': a mapping containing:
                * 'user_id'   : str, the ID of the user to update
                * 'phone'     : str, the new phone number

    Returns
    -------
    bool
        True if the update succeeded; False otherwise.
    """
    # 1. CSRF protection
    headers = request_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid CSRF token – reject the request
        return False

    # 2. Extract body parameters
    body = request_data.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("phone")

    if not user_id or not new_phone:
        # Missing required fields
        return False

    # 3. Validate phone number format (basic international E.164 compliance)
    if not PHONE_REGEX.match(new_phone):
        # Phone number does not match expected pattern
        return False

    # 4. Perform the update if user exists
    user_record = database.get(user_id)
    if not user_record:
        # User does not exist
        return False

    # Update the phone number
    user_record["phone"] = new_phone
    return True

# Example usage (for illustration only; not part of the function)
if __name__ == "__main__":
    # Populate a sample user
    database["user123"] = {"name": "Alice", "phone": "+15551234567"}

    # Craft a request
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": "user123", "phone": "+15559876543"}
    }

    result = modify_user_phone(req)
    print("Update successful:", result)          # Should print: True
    print("New phone:", database["user123"]["phone"])  # +15559876543