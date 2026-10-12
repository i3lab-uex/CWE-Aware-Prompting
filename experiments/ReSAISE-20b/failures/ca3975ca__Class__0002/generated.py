import re
from typing import Dict

# Simulated database and CSRF token
database: Dict[int, Dict[str, str]] = {}
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token-123"

# Regular expression for a simple phone number validation (digits, optional + and spaces)
PHONE_REGEX = re.compile(r"^\+?[0-9\s\-]{7,15}$")

def modify_user_phone(request_data: Dict) -> bool:
    """
    Update the phone number of a user in the simulated database.

    Args:
        request_data: A dictionary containing
            - headers['X-CSRF-Token']: CSRF token string.
            - body: a dict with keys 'user_id' (int) and 'new_phone' (str).

    Returns:
        True if the phone number was updated successfully, False otherwise.

    Raises:
        None. Errors are handled gracefully and return False.
    """
    try:
        # 1. CSRF token validation
        headers = request_data.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            return False

        # 2. Extract body data
        body = request_data.get("body", {})
        user_id = body.get("user_id")
        new_phone = body.get("new_phone")

        # 3. Validate input types
        if not isinstance(user_id, int) or not isinstance(new_phone, str):
            return False

        # 4. Validate phone number format
        if not PHONE_REGEX.fullmatch(new_phone.strip()):
            return False

        # 5. Check user existence
        if user_id not in database:
            return False

        # 6. Perform the update
        database[user_id]["phone"] = new_phone.strip()
        return True

    except Exception:
        # In a real application, log the exception here.
        return False