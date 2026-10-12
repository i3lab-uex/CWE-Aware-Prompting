import json
from typing import Dict

# Mock database: user_id -> { "phone": str, ... }
database: Dict[str, Dict] = {
    "user1": {"phone": "+15551234567", "name": "Alice"},
    "user2": {"phone": "+15559876543", "name": "Bob"},
}

# Expected CSRF token value
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123456"

def change_user_phone(request_details: Dict) -> bool:
    """
    Update a user's phone number in the mock database.

    Parameters
    ----------
    request_details : dict
        Dictionary containing HTTP headers and body. Expected structure:
            {
                "headers": {"X-CSRF-Token": "<token>"},
                "body": '{"user_id":"<id>", "new_phone":"+<digits>"}'
            }

    Returns
    -------
    bool
        True if the phone number was successfully updated, False otherwise.
    """
    # 1. Verify CSRF token presence and correctness
    headers = request_details.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        # Token missing or incorrect
        return False

    # 2. Parse body as JSON and validate required fields
    raw_body = request_details.get("body")
    if not raw_body:
        return False

    try:
        body = json.loads(raw_body)
    except json.JSONDecodeError:
        return False

    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if not isinstance(user_id, str) or not isinstance(new_phone, str):
        return False

    # Basic phone number format check (simple)
    if not new_phone.startswith("+") or not new_phone[1:].isdigit():
        return False

    # 3. Verify that the user exists in the database
    if user_id not in database:
        return False

    # 4. Perform the update
    try:
        database[user_id]["phone"] = new_phone
    except Exception:
        # Any unforeseen error results in failure
        return False

    return True