import re
from typing import Dict

# Predefined CSRF token for validation
EXPECTED_CSRF_TOKEN: str = "s3cure-t0k3n-123"

# Simulated user database
database: Dict[int, Dict[str, str]] = {
    1: {"name": "Alice", "phone": "555-0100"},
    2: {"name": "Bob",   "phone": "555-0200"},
}

def modify_user_phone(request_data: Dict) -> bool:
    """
    Update a user's phone number after validating the CSRF token.

    Parameters
    ----------
    request_data : dict
        Dictionary containing:
            - headers: dict with 'X-CSRF-Token'
            - body: dict with 'user_id' (int) and 'new_phone' (str)

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.
    """
    # 1. Validate CSRF token
    headers = request_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract and validate body data
    body = request_data.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if not isinstance(user_id, int) or not isinstance(new_phone, str):
        return False

    # Basic phone number validation: digits and optional separators
    if not re.fullmatch(r"\+?\d[\d\s\-()]*\d", new_phone):
        return False

    # 3. Update the database if user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Perform the update
    user_record["phone"] = new_phone.strip()
    return True