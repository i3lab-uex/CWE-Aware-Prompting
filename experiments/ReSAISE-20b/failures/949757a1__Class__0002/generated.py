import re
from typing import Dict

# Sample user database: {user_id: {"phone": "1234567890", ...}}
database: Dict[str, dict] = {
    "user1": {"phone": "5551234567"},
    "user2": {"phone": "5559876543"},
}

# Preconfigured CSRF token
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token-12345"

# Regular expression for a basic phone number (10 digits)
PHONE_REGEX = re.compile(r"^\d{10}$")


def change_user_contact(transaction_request: Dict) -> bool:
    """
    Update a user's phone number in the database.

    Parameters
    ----------
    transaction_request : dict
        Expected format:
            {
                "headers": {"X-CSRF-Token": "<token>"},
                "body":   {"user_id": "<id>", "new_phone": "<phone>"}
            }

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.
    """
    # 1. Verify CSRF token
    headers = transaction_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid CSRF token – reject the request
        return False

    # 2. Extract body data safely
    body = transaction_request.get("body", {})
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    # 3. Basic input validation
    if not isinstance(user_id, str) or not user_id:
        return False
    if not isinstance(new_phone, str) or not PHONE_REGEX.match(new_phone):
        return False

    # 4. Ensure the user exists
    if user_id not in database:
        return False

    # 5. Update the phone number
    try:
        database[user_id]["phone"] = new_phone
        return True
    except Exception:
        # Any unexpected error during update results in failure
        return False