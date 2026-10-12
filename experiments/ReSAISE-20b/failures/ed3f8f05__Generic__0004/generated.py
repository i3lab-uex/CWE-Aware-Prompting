import re
from typing import Dict

# Mock database and CSRF token for the example
database: Dict[int, Dict[str, str]] = {}
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token-12345"

# Simple email regex (not fully RFC compliant but sufficient for demonstration)
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
    r"(?:\.[a-zA-Z]{2,})+$)"
)

def change_user_email(request_data: Dict) -> bool:
    """
    Update a user's email address after CSRF validation and basic input checks.

    Args:
        request_data (dict): The HTTP request data containing headers, body,
                             and possibly other metadata.

    Returns:
        bool: True if the email was updated successfully, False otherwise.
    """
    # 1. CSRF token validation
    headers = request_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF token missing or invalid
        return False

    # 2. Extract user_id and new_email from body
    body = request_data.get("body", {})
    try:
        user_id_raw = body["user_id"]
        new_email = body["new_email"].strip()
    except KeyError:
        # Required fields are missing
        return False

    # 3. Validate user_id type and existence in database
    try:
        user_id = int(user_id_raw)
    except (TypeError, ValueError):
        return False

    if user_id not in database:
        # User does not exist
        return False

    # 4. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 5. Perform the update
    try:
        database[user_id]["email"] = new_email
    except Exception:
        # Catch any unexpected errors during the update
        return False

    return True