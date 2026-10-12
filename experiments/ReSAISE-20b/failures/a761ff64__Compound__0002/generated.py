import re
from typing import Dict

# Simulated environment constants
EXPECTED_CSRF_TOKEN = "secure-token-12345"
database: Dict[str, Dict] = {
    # Example user entries
    "user1": {"phone": "+1234567890", "name": "Alice"},
    "user2": {"phone": "+0987654321", "name": "Bob"},
}


def alter_user_phone(input: Dict) -> bool:
    """
    Update the phone number of a specific user.

    Args:
        input (dict): A request dictionary containing:
            - headers: dict with the CSRF token under key 'X-CSRF-Token'
            - body: dict with keys:
                * 'user_id'   (str): The ID of the user to update
                * 'new_phone' (str): The new phone number

    Returns:
        bool: True if the update succeeded, False otherwise.
    """
    # Validate top‑level structure
    headers = input.get("headers")
    body = input.get("body")

    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # CSRF protection
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # Extract and validate payload
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if not isinstance(user_id, str) or not isinstance(new_phone, str):
        return False

    # Basic phone format validation (allow + and digits)
    if not re.fullmatch(r"\+?\d{7,15}", new_phone):
        return False

    # Check that the user exists
    user_record = database.get(user_id)
    if user_record is None:
        return False

    # Perform the update
    try:
        user_record["phone"] = new_phone
        return True
    except Exception:
        # Any unexpected error results in failure
        return False


# Example usage (uncomment to test)
# request = {
#     "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
#     "body": {"user_id": "user1", "new_phone": "+1112223333"}
# }
# print(alter_user_phone(request))