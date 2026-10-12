import re
from typing import Dict

# Sample in‑memory database (user_id -> user data)
database: Dict[str, Dict] = {
    "u123": {"name": "Alice", "phone": "+15551234567"},
    "u456": {"name": "Bob",   "phone": "+15559876543"},
}

# Pre‑configured CSRF token (in a real app this would be stored securely)
EXPECTED_CSRF_TOKEN: str = "a1b2c3d4e5f6g7h8"

# Regular expression for a simple international phone number (E.164 format)
PHONE_REGEX = re.compile(r"^\+\d{10,15}$")


def change_user_contact(transaction_request: Dict) -> bool:
    """
    Update the phone number of a user in ``database``.
    
    Parameters
    ----------
    transaction_request : dict
        Expected structure:
            {
                "headers": {"X-CSRF-Token": "<token>"},
                "body":    {
                    "user_id":      "<string>",
                    "new_phone":    "+<digits>"
                }
            }

    Returns
    -------
    bool
        ``True`` if the phone number was updated, otherwise ``False``.

    Notes
    -----
    * Validates the CSRF token to protect against cross‑site request forgery.
    * Checks that ``user_id`` exists in the database.
    * Validates the new phone number against a simple E.164 regex.
    """
    # 1) Validate request structure
    if not isinstance(transaction_request, dict):
        return False

    headers = transaction_request.get("headers")
    body = transaction_request.get("body")

    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # 2) CSRF token check (CWE‑693)
    csrf_token = headers.get("X-CSRF-Token")
    if not isinstance(csrf_token, str) or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 3) Extract user ID and new phone number
    user_id = body.get("user_id")
    new_phone = body.get("new_phone")

    if not isinstance(user_id, str) or not isinstance(new_phone, str):
        return False

    # 4) Validate phone number format
    if not PHONE_REGEX.match(new_phone):
        return False

    # 5) Update the database
    user_record = database.get(user_id)
    if user_record is None:
        return False

    # Perform the update atomically
    try:
        user_record["phone"] = new_phone
    except Exception:  # pragma: no cover
        return False

    return True


# Example usage (for testing purposes)
if __name__ == "__main__":
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {
            "user_id": "u123",
            "new_phone": "+15550123456"
        }
    }

    success = change_user_contact(req)
    print("Update succeeded:", success)
    print("Updated database entry:", database["u123"])