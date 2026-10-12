import json
from typing import Dict

# Mock database and CSRF token for demonstration purposes
database: Dict[int, Dict[str, str]] = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+0987654321"},
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"


def alter_user_phone(incoming_request: Dict) -> bool:
    """
    Update a user's phone number after validating the CSRF token and request data.

    Parameters
    ----------
    incoming_request : dict
        Dictionary representing the HTTP request. Expected keys:
            - 'headers': dict containing HTTP headers.
            - 'body'   : str or bytes with JSON payload.

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    # 1. Basic request structure check
    if not isinstance(incoming_request, dict):
        return False

    headers = incoming_request.get("headers")
    body = incoming_request.get("body")

    if not isinstance(headers, dict) or body is None:
        return False

    # 2. CSRF token validation (CWE-352 mitigation)
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 3. Parse body JSON safely
    try:
        if isinstance(body, bytes):
            body = body.decode("utf-8")
        payload = json.loads(body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return False

    # 4. Extract required fields
    user_id = payload.get("user_id")
    new_phone = payload.get("new_phone")

    if not isinstance(user_id, int) or not isinstance(new_phone, str):
        return False

    # 5. Validate phone number format (simple regex check)
    import re
    if not re.fullmatch(r"\+\d{7,15}", new_phone):
        return False

    # 6. Perform the update in the mock database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Optional: ensure the new phone number is different
    if user_record.get("phone") == new_phone:
        return True  # nothing to change, but still considered successful

    user_record["phone"] = new_phone
    return True