import re
from typing import Dict

# Sample user database (user_id -> user data)
database: Dict[str, Dict] = {
    "1": {"name": "Alice", "phone": "+15551234567"},
    "2": {"name": "Bob",   "phone": "+15559876543"},
}

# Expected CSRF token for validation
EXPECTED_CSRF_TOKEN: str = "s3cr3t-csrf-token"

# Regular expression for a basic international phone number (E.164 format)
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")


def change_user_contact(transaction_request: Dict) -> bool:
    """
    Update the phone number of a user in the database.

    Parameters
    ----------
    transaction_request : dict
        Expected to contain:
            - 'headers': dict with a 'X-CSRF-Token' key
            - 'body': dict with keys:
                * 'user_id' : str
                * 'new_phone' : str

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.
    """
    # 1. Validate CSRF token
    headers = transaction_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid CSRF token – reject the request
        return False

    # 2. Extract body data safely
    body = transaction_request.get("body", {})
    user_id = str(body.get("user_id", "")).strip()
    new_phone = str(body.get("new_phone", "")).strip()

    if not user_id or not new_phone:
        # Missing required fields
        return False

    # 3. Validate phone number format
    if not PHONE_REGEX.match(new_phone):
        return False

    # 4. Update the database if user exists
    user_record = database.get(user_id)
    if not user_record:
        # User ID does not exist
        return False

    # 5. Perform the update (no side effects beyond the in‑memory dict)
    user_record["phone"] = new_phone
    return True


# Example usage (for testing purposes)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": "1", "new_phone": "+15550000000"},
    }
    result = change_user_contact(request)
    print("Update successful:", result)
    print("Updated database entry:", database["1"])