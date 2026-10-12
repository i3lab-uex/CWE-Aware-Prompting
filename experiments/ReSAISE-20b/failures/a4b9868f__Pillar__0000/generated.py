import re
from typing import Dict, Any

# Preconfigured CSRF token (example value)
EXPECTED_CSRF_TOKEN = "secure_csrf_token_12345"

def alter_user_phone(service_request: Dict[str, Any], database: Dict[int, Dict[str, Any]]) -> bool:
    """
    Update a user's phone number in the database after validating the CSRF token.

    Parameters
    ----------
    service_request : dict
        Dictionary containing 'headers' and 'body'. The body must include:
            - 'user_id': int
            - 'new_phone': str (digits only, optional formatting characters)
    database : dict
        Mapping of user_id to a dictionary of user attributes.

    Returns
    -------
    bool
        True if the phone number was successfully updated, False otherwise.
    """
    # 1. Validate CSRF token
    headers = service_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token") or headers.get("csrf-token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract user ID and new phone number
    body = service_request.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_phone_raw = str(body["new_phone"])
    except (KeyError, ValueError):
        return False

    # 3. Sanitize and validate phone number (digits only, length 10-15)
    new_phone = re.sub(r"[^\d]", "", new_phone_raw)  # strip non-digits
    if not (10 <= len(new_phone) <= 15):
        return False

    # 4. Update the database if user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 5. Perform the update
    try:
        user_record["phone"] = new_phone
        return True
    except Exception:
        # Any unexpected error (e.g., read-only dict) results in failure
        return False