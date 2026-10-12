import json
from typing import Dict, Any

# Mock database and expected CSRF token for demonstration purposes.
database: Dict[str, Dict[str, Any]] = {}
EXPECTED_CSRF_TOKEN: str = "expected_csrf_token_value"


def alter_user_phone(incoming_request: Dict[str, Any]) -> bool:
    """
    Update a user's phone number in the mock database.

    Parameters
    ----------
    incoming_request : dict
        Dictionary containing 'headers' and 'body'. Expected structure:
            {
                "headers": {"X-CSRF-Token": "<token>"},
                "body":   {"user_id": "<id>", "phone_number": "<new_phone>"}
            }

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    # 1. CSRF token validation
    headers = incoming_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body data
    body = incoming_request.get("body", {})
    if not isinstance(body, dict):
        return False

    user_id = body.get("user_id")
    new_phone = body.get("phone_number")

    if not user_id or not new_phone:
        return False

    # 3. Validate phone number format (basic check)
    if not isinstance(new_phone, str) or not new_phone.isdigit() or len(new_phone) < 7:
        return False

    # 4. Check if user exists
    user_record = database.get(str(user_id))
    if not user_record:
        return False

    # 5. Perform the update
    try:
        user_record["phone_number"] = new_phone
        return True
    except Exception:
        # Any unexpected error results in a failure flag.
        return False


# Example usage (for testing purposes only)
if __name__ == "__main__":
    # Populate mock database
    database["123"] = {"name": "Alice", "phone_number": "5551234"}

    # Construct a valid request
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": "123", "phone_number": "9876543"}
    }

    print(alter_user_phone(req))  # Expected: True
    print(database["123"]["phone_number"])  # Expected: '9876543'