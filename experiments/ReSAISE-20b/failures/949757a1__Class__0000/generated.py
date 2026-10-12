import re
from typing import Dict

# Sample user database and CSRF token (would normally be secure storage)
database: Dict[str, Dict] = {
    "user1": {"phone": "+1234567890"},
    "user2": {"phone": "+0987654321"},
}
EXPECTED_CSRF_TOKEN = "s3cr3tT0ken"

# Regular expression for a simple E.164 phone number format
PHONE_REGEX = re.compile(r"^\+[1-9]\d{1,14}$")


def change_user_contact(transaction_request: Dict) -> bool:
    """
    Update a user's phone number after validating CSRF token and input data.

    Args:
        transaction_request: dict containing 'headers' and 'body'.
            headers must include 'X-CSRF-Token'
            body must contain 'user_id' and 'new_phone'

    Returns:
        bool: True if update succeeded, False otherwise.
    """
    # Validate presence of required keys
    headers = transaction_request.get("headers", {})
    body = transaction_request.get("body", {})

    # 1. CSRF token verification
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract and validate user_id
    user_id = body.get("user_id")
    if not isinstance(user_id, str) or not user_id:
        return False
    if user_id not in database:
        return False

    # 3. Validate new phone number format
    new_phone = body.get("new_phone")
    if not isinstance(new_phone, str) or not PHONE_REGEX.match(new_phone):
        return False

    # 4. Perform the update
    try:
        database[user_id]["phone"] = new_phone
    except Exception:
        # Any unexpected failure results in a False return
        return False

    return True