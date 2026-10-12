import json
from typing import Dict

# Sample database and CSRF token configuration
database: Dict[str, dict] = {
    "user1": {"phone": "+1234567890"},
    "user2": {"phone": "+0987654321"},
}
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_123"

def modify_user_phone(user_request: Dict) -> bool:
    """
    Update a user's phone number in the `database` based on an incoming request.

    Parameters
    ----------
    user_request : dict
        A dictionary containing:
            - 'headers': a dict of request headers.
            - 'body': a JSON string with keys 'user_id' and 'new_phone'.

    Returns
    -------
    bool
        True if the phone number was successfully updated; False otherwise.
    """
    # Validate CSRF token
    headers = user_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # Parse body
    body = user_request.get("body")
    if not isinstance(body, str):
        return False

    try:
        data = json.loads(body)
    except (json.JSONDecodeError, TypeError):
        return False

    user_id = data.get("user_id")
    new_phone = data.get("new_phone")

    # Basic validation of inputs
    if not isinstance(user_id, str) or not isinstance(new_phone, str):
        return False

    # Simple phone number format check (digits and optional +)
    if not (new_phone.startswith("+") or new_phone[0].isdigit()) or not all(ch.isdigit() for ch in new_phone.lstrip("+")):
        return False

    # Update database if user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    user_record["phone"] = new_phone
    return True