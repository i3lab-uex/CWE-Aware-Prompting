import re
from typing import Dict

# Expected CSRF token for validation
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token-123"

# Simulated user database
# Example structure: {user_id: {"name": "Alice", "phone": "+1234567890"}}
database: Dict[int, Dict[str, str]] = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"},
}


def _is_valid_phone_number(phone: str) -> bool:
    """
    Very simple phone number validation.
    Accepts digits, optional leading '+', and length between 7 and 15.
    """
    return bool(re.fullmatch(r"\+?\d{7,15}", phone))


def modify_user_phone(request_data: Dict) -> bool:
    """
    Update the phone number of a user.

    Parameters
    ----------
    request_data : dict
        Expected structure:
            {
                "headers": {"X-CSRF-Token": "<token>"},
                "body":    {"user_id": <int>, "new_phone": "<string>"}
            }

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    # Validate CSRF token
    headers = request_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # Extract body parameters
    body = request_data.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    # Basic checks
    if not isinstance(user_id, int) or not isinstance(new_phone, str):
        return False

    # Validate phone number format
    if not _is_valid_phone_number(new_phone):
        return False

    # Check user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Perform the update
    user_record["phone"] = new_phone
    return True


# Example usage (for testing purposes only)
if __name__ == "__main__":
    sample_request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body":    {"user_id": 1, "new_phone": "+15551234567"},
    }
    result = modify_user_phone(sample_request)
    print("Update successful:", result)
    print("Updated record:", database[1])