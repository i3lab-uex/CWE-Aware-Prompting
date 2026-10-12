import json
import re

# Sample database and CSRF token for illustration purposes
database = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"}
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

def _is_valid_phone(phone: str) -> bool:
    """
    Very simple phone validation. Adjust regex for real-world use.
    """
    pattern = re.compile(r"^\+\d{10,15}$")
    return bool(pattern.match(phone))

def modify_user_phone(user_request: dict) -> bool:
    """
    Update a user's phone number after validating CSRF token and input data.

    Parameters
    ----------
    user_request : dict
        A dictionary containing 'headers' and 'body'.
        The body is expected to be a JSON string with keys:
            - user_id : int
            - new_phone : str

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    # 1. Validate CSRF token
    headers = user_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token") or headers.get("x-csrf-token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF token missing or invalid
        return False

    # 2. Parse request body
    body = user_request.get("body")
    if not body:
        return False

    try:
        payload = json.loads(body)
    except (json.JSONDecodeError, TypeError):
        return False

    # 3. Extract and validate required fields
    user_id = payload.get("user_id")
    new_phone = payload.get("new_phone")

    if not isinstance(user_id, int) or not isinstance(new_phone, str):
        return False

    if not _is_valid_phone(new_phone):
        return False

    # 4. Update database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Perform the update
    user_record["phone"] = new_phone
    return True