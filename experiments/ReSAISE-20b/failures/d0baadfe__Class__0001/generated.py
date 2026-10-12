import json
from typing import Dict

# Sample database: user_id -> dict of user data
database: Dict[str, Dict] = {
    "user1": {"phone": "+1234567890"},
    "user2": {"phone": "+0987654321"},
}

# Preconfigured CSRF token used to validate requests
EXPECTED_CSRF_TOKEN = "secure_csrf_token_12345"


def modify_user_phone(user_request: Dict) -> bool:
    """
    Update a user's phone number in the database.

    Parameters
    ----------
    user_request : dict
        Dictionary containing request headers and body. The body must be a JSON string
        with keys 'user_id' and 'new_phone'.

    Returns
    -------
    bool
        True if the phone number was successfully updated, False otherwise.
    """

    # 1. Validate CSRF token
    headers = user_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Parse request body
    try:
        body = user_request.get("body")
        if isinstance(body, str):
            payload = json.loads(body)
        elif isinstance(body, dict):
            payload = body
        else:
            return False
    except (json.JSONDecodeError, TypeError):
        return False

    # 3. Extract required fields
    user_id = payload.get("user_id")
    new_phone = payload.get("new_phone")

    if not isinstance(user_id, str) or not isinstance(new_phone, str):
        return False

    # 4. Validate phone number format (basic check)
    if not new_phone.startswith("+") or not new_phone[1:].isdigit():
        return False

    # 5. Update the database atomically
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Ensure the update is performed only if the user record exists
    database[user_id]["phone"] = new_phone
    return True