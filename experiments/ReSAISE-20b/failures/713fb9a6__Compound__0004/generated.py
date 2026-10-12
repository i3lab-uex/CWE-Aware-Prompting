import re
from typing import Dict

# Simulated database: user_id -> user record dict
database: Dict[str, Dict] = {
    "1": {"name": "Alice", "phone": "+1234567890"},
    "2": {"name": "Bob",   "phone": "+0987654321"},
}

# Predefined CSRF token that must match the request
EXPECTED_CSRF_TOKEN: str = "secure-unique-csrf-token"

# Regular expression for a simple phone number validation
PHONE_REGEX = re.compile(r"^\+?[1-9]\d{7,14}$")  # E.164 format


def change_user_phone(payload: Dict) -> bool:
    """
    Update the phone number for a user identified by `user_id` in the payload.

    Args:
        payload: A dictionary containing two top‑level keys:
            * `headers`: a dict with the key `csrf_token`
            * `body`: a dict containing `user_id` and `phone`

    Returns:
        True if the phone number was updated successfully,
        False otherwise.

    Raises:
        None
    """
    # --- 1. CSRF validation --------------------------------------------
    headers = payload.get("headers", {})
    token = headers.get("csrf_token")
    if token != EXPECTED_CSRF_TOKEN:
        # CSRF check failed – do not proceed
        return False

    # --- 2. Extract payload data ---------------------------------------
    body = payload.get("body", {})
    user_id = str(body.get("user_id"))  # ensure string key
    new_phone = body.get("phone")

    if not user_id or not new_phone:
        # Missing required fields
        return False

    # --- 3. Phone number format validation -----------------------------
    if not PHONE_REGEX.match(new_phone):
        # Invalid phone format
        return False

    # --- 4. Database lookup and update ---------------------------------
    user_record = database.get(user_id)
    if not user_record:
        # User does not exist
        return False

    # Update the phone number atomically (simulate)
    user_record["phone"] = new_phone
    return True


# ----------------------------------------------------------------------
# Example usage (for testing purposes only; remove or comment out in production)
if __name__ == "__main__":
    test_payload = {
        "headers": {"csrf_token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": "1", "phone": "+15551234567"},
    }
    result = change_user_phone(test_payload)
    print("Update successful:", result)
    print("Updated record:", database["1"])