import re

# Predefined CSRF token for validation
EXPECTED_CSRF_TOKEN = "secure_csrf_token_123"

# Simulated user database: {user_id: {"phone": "..."}, ...}
database = {
    1: {"phone": "+1234567890"},
    2: {"phone": "+1987654321"},
}

def modify_user_phone(request_data):
    """
    Update a user's phone number in the simulated database.

    Parameters
    ----------
    request_data : dict
        A dictionary containing:
            - 'headers': a dict with the CSRF token under key 'X-CSRF-Token'
            - 'body': a dict with keys:
                * 'user_id' (int)
                * 'new_phone' (str)

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.
    """
    try:
        # 1. Verify CSRF token
        headers = request_data.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            return False

        # 2. Extract body parameters
        body = request_data.get("body", {})
        user_id = body.get("user_id")
        new_phone = body.get("new_phone")

        if user_id is None or new_phone is None:
            return False

        # 3. Validate phone number format (simple E.164 check)
        if not isinstance(new_phone, str) or not re.fullmatch(r"\+[1-9]\d{7,14}", new_phone):
            return False

        # 4. Ensure user exists
        if user_id not in database:
            return False

        # 5. Update phone number atomically
        database[user_id]["phone"] = new_phone

        return True

    except Exception:
        # Any unexpected error should result in a safe failure
        return False