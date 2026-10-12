import json
from typing import Dict, Any

# Mock database and expected CSRF token (would normally be stored securely)
database: Dict[int, Dict[str, Any]] = {}
EXPECTED_CSRF_TOKEN: str = "expected_csrf_token_value"
ALLOWED_ORIGINS = {"https://trusted.example.com"}

def modify_user_phone(client_request: Dict[str, Any]) -> bool:
    """
    Update a user's phone number in the mock database.

    Parameters
    ----------
    client_request : dict
        The HTTP request representation. Expected to contain:
            - 'headers': mapping of header names to values
            - 'body': JSON string with keys:
                * 'user_id' (int)
                * 'new_phone' (str)

    Returns
    -------
    bool
        True if the phone number was updated, False otherwise.
    """

    # 1. Basic request structure validation
    if not isinstance(client_request, dict):
        return False

    headers = client_request.get("headers", {})
    body_raw = client_request.get("body")

    if not isinstance(headers, dict) or body_raw is None:
        return False

    # 2. CSRF token verification (CWE-345 mitigation)
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 3. Origin header check to ensure request comes from a trusted source
    origin = headers.get("Origin")
    if origin not in ALLOWED_ORIGINS:
        return False

    # 4. Parse the JSON body safely
    try:
        body = json.loads(body_raw)
    except (json.JSONDecodeError, TypeError):
        return False

    # 5. Validate required fields and types
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if not isinstance(user_id, int) or not isinstance(new_phone, str):
        return False

    # 6. Basic phone number format check (simple regex)
    if not new_phone.isdigit() or len(new_phone) < 7:
        return False

    # 7. Perform the update if user exists
    user_record = database.get(user_id)
    if not isinstance(user_record, dict):
        return False

    # 8. Update the phone number
    user_record["phone"] = new_phone
    return True