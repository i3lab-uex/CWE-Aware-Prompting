import re
import hmac

# Mock database and CSRF token (would normally be stored securely)
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+0987654321"}
}
EXPECTED_CSRF_TOKEN = "secure_expected_token_value"

# Regular expression for a simple international phone number (E.164 format)
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")

def alter_user_phone(incoming_request: dict) -> bool:
    """
    Update a user's phone number after verifying CSRF token and input format.

    Parameters
    ----------
    incoming_request : dict
        Dictionary containing 'headers' and 'body'.
        Expected structure:
            {
                "headers": {"X-CSRF-Token": "<token_value>"},
                "body":    {
                    "user_id": <int>,
                    "new_phone": "<phone_number>"
                }
            }

    Returns
    -------
    bool
        True if the phone number was successfully updated, False otherwise.
    """
    # 1. Basic request validation
    if not isinstance(incoming_request, dict):
        return False

    headers = incoming_request.get("headers", {})
    body = incoming_request.get("body", {})

    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # 2. CSRF token verification (constant‑time comparison)
    csrf_token = headers.get("X-CSRF-Token")
    if not isinstance(csrf_token, str):
        return False
    if not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # 3. Extract and validate user ID
    user_id = body.get("user_id")
    if not isinstance(user_id, int):
        return False
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 4. Validate new phone number format
    new_phone = body.get("new_phone")
    if not isinstance(new_phone, str) or not PHONE_REGEX.match(new_phone):
        return False

    # 5. Perform the update
    try:
        user_record["phone"] = new_phone
        return True
    except Exception:
        # Any unexpected error during update results in failure
        return False

# Example usage (for testing purposes only)
if __name__ == "__main__":
    req = {
        "headers": {"X-CSRF-Token": "secure_expected_token_value"},
        "body":    {"user_id": 1, "new_phone": "+15551234567"}
    }
    print(alter_user_phone(req))          # Expected: True
    print(database[1]["phone"])           # Updated phone number