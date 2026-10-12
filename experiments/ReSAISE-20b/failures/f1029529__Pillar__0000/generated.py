import re
from typing import Dict, Any

# Mock database and CSRF token for demonstration purposes.
database: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+0987654321"},
}
EXPECTED_CSRF_TOKEN = "expected_csrf_token_value"

# Regular expression for a simple international phone number validation.
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")


def modify_user_phone(client_request: Dict[str, Any]) -> bool:
    """
    Update a user's phone number in the mock database.

    Parameters
    ----------
    client_request : dict
        The request payload containing headers and a body with:
            - "user_id": int, the identifier of the user to update
            - "new_phone": str, the new phone number in E.164 format
        and a header:
            - "X-CSRF-Token": str, CSRF protection token

    Returns
    -------
    bool
        True if the update was successful, False otherwise.

    Raises
    ------
    ValueError
        If required fields are missing or invalid.
    """
    # 1. CSRF protection: ensure the token matches the expected value.
    headers = client_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Log the incident in a real system; here we simply return False.
        return False

    # 2. Validate request body structure.
    body = client_request.get("body")
    if not isinstance(body, dict):
        return False

    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    # 3. Validate user ID: must be an integer and exist in the database.
    if not isinstance(user_id, int) or user_id not in database:
        return False

    # 4. Validate phone number format.
    if not isinstance(new_phone, str) or not PHONE_REGEX.match(new_phone):
        return False

    # 5. Perform the update atomically (simplified for mock DB).
    try:
        database[user_id]["phone"] = new_phone
        return True
    except Exception:
        # In a real scenario, log the exception details securely.
        return False