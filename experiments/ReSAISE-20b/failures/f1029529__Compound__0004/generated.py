import re

# Mock database and expected CSRF token (for illustration purposes)
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"}
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

# Regular expression for a basic international phone number (e.g., +1234567890)
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")

def modify_user_phone(client_request: dict) -> bool:
    """
    Update a user's phone number in the mock database.

    Parameters
    ----------
    client_request : dict
        Dictionary containing request headers and body. Expected structure:
            {
                "headers": {"X-CSRF-Token": "<token>"},
                "body":   {
                    "user_id"     : <int>,
                    "new_phone"   : "<string>"
                }
            }

    Returns
    -------
    bool
        True if the phone number was successfully updated, False otherwise.
    """
    try:
        # 1. CSRF protection: validate the token
        headers = client_request.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            # Invalid or missing CSRF token
            return False

        # 2. Extract and validate payload
        body = client_request.get("body", {})
        user_id = body.get("user_id")
        new_phone = body.get("new_phone")

        # Ensure user_id is an integer and exists in the database
        if not isinstance(user_id, int) or user_id not in database:
            return False

        # Validate phone number format
        if not isinstance(new_phone, str) or not PHONE_REGEX.match(new_phone):
            return False

        # 3. Perform the update
        database[user_id]["phone"] = new_phone
        return True

    except Exception:
        # In a real application, log the exception details.
        return False