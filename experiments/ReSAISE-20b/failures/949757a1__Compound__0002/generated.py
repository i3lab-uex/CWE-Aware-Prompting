import json
from typing import Dict

# Sample user database and CSRF token (in a real app these would be secure)
database: Dict[int, Dict[str, str]] = {
    1: {"name": "Alice", "phone": "+123456789"},
    2: {"name": "Bob",   "phone": "+987654321"}
}
EXPECTED_CSRF_TOKEN: str = "s3cr3t-t0ken"

def change_user_contact(transaction_request: Dict) -> bool:
    """
    Update a user's phone number in the database after validating
    the CSRF token and request payload.

    Parameters
    ----------
    transaction_request : dict
        Must contain a 'headers' key with the CSRF token under
        'X-CSRF-Token', and a 'body' key with a JSON string
        holding 'user_id' (int) and 'new_phone' (str).

    Returns
    -------
    bool
        True if the phone number was updated successfully,
        False otherwise.
    """
    # 1. CSRF validation
    headers = transaction_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Parse and validate body
    raw_body = transaction_request.get("body")
    if not raw_body:
        return False

    try:
        body = json.loads(raw_body)
    except (json.JSONDecodeError, TypeError):
        return False

    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if not isinstance(user_id, int) or not isinstance(new_phone, str):
        return False

    # 3. Update database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Basic phone format check (simple regex: starts with + and digits)
    import re
    if not re.fullmatch(r"\+\d{7,15}", new_phone):
        return False

    # Perform the update
    user_record["phone"] = new_phone
    return True