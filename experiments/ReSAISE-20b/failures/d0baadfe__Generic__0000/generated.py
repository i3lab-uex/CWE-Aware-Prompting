import re
from typing import Dict

# Sample in‑memory database of users.
# Keys are user IDs (int), values are dicts with a 'phone' field.
database: Dict[int, Dict[str, str]] = {
    1: {"phone": "555-0100"},
    2: {"phone": "555-0200"},
    3: {"phone": "555-0300"},
}

# Preconfigured CSRF token used by the application.
EXPECTED_CSRF_TOKEN: str = "my_secure_csrf_token"


def _validate_phone_number(phone: str) -> bool:
    """
    Basic phone number validation. Accepts numbers, spaces, dashes,
    parentheses and plus signs. This is intentionally permissive
    but still filters out obvious invalid input.
    """
    pattern = re.compile(r"^[\d\s()+-]{7,20}$")
    return bool(pattern.match(phone))


def modify_user_phone(user_request: Dict) -> bool:
    """
    Update the phone number for a user in the database.

    Parameters
    ----------
    user_request : dict
        Expected structure:
            {
                "headers": {"X-CSRF-Token": "<token>"},
                "body":   {
                    "user_id": int,
                    "phone":   str
                }
            }

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.
    """
    # 1. Validate CSRF token
    headers = user_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body data
    body = user_request.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_phone = str(body["phone"]).strip()
    except (KeyError, ValueError, TypeError):
        return False

    # 3. Validate phone format
    if not _validate_phone_number(new_phone):
        return False

    # 4. Update the database if user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    user_record["phone"] = new_phone
    return True


# Example usage (for testing purposes)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": "my_secure_csrf_token"},
        "body": {"user_id": 2, "phone": "+1 (555) 123-4567"},
    }
    print(modify_user_phone(request))  # Expected: True
    print(database[2]["phone"])        # Updated phone number