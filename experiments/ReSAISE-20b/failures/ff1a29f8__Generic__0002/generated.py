import json
import re
from typing import Dict

# Mock database and CSRF token
database: Dict[int, Dict[str, str]] = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"}
}
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token-123"

def _is_valid_phone(phone: str) -> bool:
    """
    Very simple phone validation: international format with optional + and digits.
    Adjust as needed for stricter checks (e.g., length, country codes).
    """
    return bool(re.fullmatch(r"\+?\d{7,15}", phone))

def change_user_phone(request_details: Dict) -> bool:
    """
    Update a user's phone number in the mock database.

    Parameters
    ----------
    request_details : dict
        Expected keys:
            - headers: dict, must contain 'X-CSRF-Token'
            - body   : str or bytes, JSON string with keys:
                * user_id (int)
                * new_phone (str)

    Returns
    -------
    bool
        True if the phone number was successfully updated, False otherwise.
    """
    # 1. CSRF token validation
    headers = request_details.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Parse request body
    raw_body = request_details.get("body")
    if isinstance(raw_body, bytes):
        try:
            raw_body = raw_body.decode("utf-8")
        except UnicodeDecodeError:
            return False
    if not isinstance(raw_body, str):
        return False

    try:
        payload = json.loads(raw_body)
    except json.JSONDecodeError:
        return False

    user_id = payload.get("user_id")
    new_phone = payload.get("new_phone")

    if not isinstance(user_id, int) or not isinstance(new_phone, str):
        return False

    # 3. Validate phone number format
    if not _is_valid_phone(new_phone):
        return False

    # 4. Update the database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Ensure that we don't accidentally create new keys
    if "phone" not in user_record:
        return False

    # Perform the update atomically
    try:
        user_record["phone"] = new_phone
    except Exception:
        return False

    return True