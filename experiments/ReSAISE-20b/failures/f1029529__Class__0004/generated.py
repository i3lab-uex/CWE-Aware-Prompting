import re

# Mock database and CSRF token for demonstration purposes
database = {
    1: {"name": "Alice", "phone": "+15551234567"},
    2: {"name": "Bob",   "phone": "+15559876543"},
}
EXPECTED_CSRF_TOKEN = "secure-token-123"

# Regular expression for a simple international phone number validation
PHONE_REGEX = re.compile(r"^\+?[1-9]\d{1,14}$")  # E.164 format


def modify_user_phone(client_request: dict) -> bool:
    """
    Update a user's phone number in the mock database.

    Parameters
    ----------
    client_request : dict
        Expected structure:
            {
                "headers": {"X-CSRF-Token": "<token>", ...},
                "body":   {
                    "user_id": <int>,
                    "new_phone": "<string>"
                }
            }

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    try:
        # 1. Verify CSRF token
        headers = client_request.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
        if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
            return False

        # 2. Extract and validate payload
        body = client_request.get("body", {})
        user_id = body.get("user_id")
        new_phone = body.get("new_phone")

        # Basic type checks
        if not isinstance(user_id, int) or not isinstance(new_phone, str):
            return False

        # 3. Validate phone number format
        if not PHONE_REGEX.match(new_phone):
            return False

        # 4. Check user existence
        if user_id not in database:
            return False

        # 5. Update phone number
        database[user_id]["phone"] = new_phone
        return True

    except Exception:
        # Catch-all to avoid leaking stack traces; in production
        # use specific exception handling and logging.
        return False