import re
from typing import Dict

# Sample context (would normally be provided by the application)
database: Dict[int, Dict[str, str]] = {
    1: {"name": "Alice", "phone": "5551234"},
    2: {"name": "Bob",   "phone": "5555678"},
}
EXPECTED_CSRF_TOKEN = "securetoken123"


def alter_user_phone(service_request: Dict) -> bool:
    """
    Update a user's phone number in the database.

    Parameters
    ----------
    service_request : dict
        Dictionary containing 'headers' and 'body'.  The body must contain:
          - 'user_id': int
          - 'new_phone': str

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    # 1. Validate CSRF token
    headers = service_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body data
    body = service_request.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_phone = body["new_phone"]
    except (KeyError, ValueError, TypeError):
        return False

    # 3. Validate phone number format (simple: digits only, length 7-15)
    if not re.fullmatch(r"\d{7,15}", new_phone):
        return False

    # 4. Check user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 5. Perform the update
    try:
        user_record["phone"] = new_phone
        return True
    except Exception:
        # In a real system we might log the exception
        return False