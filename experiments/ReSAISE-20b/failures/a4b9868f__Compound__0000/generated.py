import re

# Sample user database: {user_id: {"phone": "..."}}
database = {
    1: {"phone": "555-0100"},
    2: {"phone": "555-0200"},
}

# Preconfigured CSRF token that must match the request header
EXPECTED_CSRF_TOKEN = "secure_csrf_token_12345"

# Regular expression for a basic phone number format (e.g., 10 digits)
PHONE_REGEX = re.compile(r"^\+?\d{7,15}$")

def alter_user_phone(service_request: dict) -> bool:
    """
    Update a user's phone number in the database after validating CSRF token
    and ensuring the new phone number is well‑formed.

    Parameters:
        service_request (dict): Expected to contain a 'headers' dict with
                                a 'X-CSRF-Token' key and a 'body' dict that
                                includes 'user_id' (int) and 'new_phone'
                                (str).

    Returns:
        bool: True if the phone number was updated successfully, False otherwise.
    """
    # 1. Validate CSRF token
    headers = service_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid CSRF token
        return False

    # 2. Extract body payload
    body = service_request.get("body", {})
    if not isinstance(body, dict):
        return False

    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    # 3. Validate user ID and phone number presence
    if not isinstance(user_id, int) or not isinstance(new_phone, str):
        return False

    # 4. Validate phone number format
    if not PHONE_REGEX.match(new_phone):
        return False

    # 5. Ensure user exists in the database
    if user_id not in database:
        return False

    # 6. Update the phone number
    try:
        database[user_id]["phone"] = new_phone
        return True
    except Exception:
        # In a real application, log the exception here.
        return False

# Example usage (for testing purposes only)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_phone": "+15551234567"},
    }
    print(alter_user_phone(request))  # Should output: True
    print(database[1]["phone"])       # Should show the updated phone number