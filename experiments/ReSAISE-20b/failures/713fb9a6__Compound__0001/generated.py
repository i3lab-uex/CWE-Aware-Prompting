import re
from typing import Dict, Any

# Simulated global database and CSRF token for the application
database: Dict[int, Dict[str, Any]] = {}
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token-12345"

def _is_valid_phone(phone: str) -> bool:
    """
    Basic phone number validation.
    Accepts digits, optional leading '+', and length between 7 and 15.
    """
    pattern = re.compile(r"^\+?\d{7,15}$")
    return bool(pattern.match(phone))

def change_user_phone(payload: Dict[str, Any]) -> bool:
    """
    Update the phone number of a user in the simulated database.

    Parameters
    ----------
    payload : dict
        Expected to contain:
            - headers: dict with 'X-CSRF-Token' key.
            - body: dict with 'user_id' (int) and 'new_phone' (str).

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.

    Raises
    ------
    ValueError
        If the payload structure is incorrect or validation fails.
    """
    # 1. CSRF protection
    try:
        csrf_token = payload["headers"]["X-CSRF-Token"]
    except KeyError:
        raise ValueError("Missing CSRF token in headers")

    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Potential CSRF attack
        return False

    # 2. Payload validation
    try:
        body = payload["body"]
        user_id = int(body["user_id"])
        new_phone = str(body["new_phone"])
    except (KeyError, TypeError, ValueError):
        raise ValueError("Invalid payload structure or data types")

    # 3. Phone number format validation
    if not _is_valid_phone(new_phone):
        raise ValueError("Invalid phone number format")

    # 4. Update the database
    if user_id not in database:
        return False

    # Perform the update atomically (in a real DB you'd use transactions)
    database[user_id]["phone"] = new_phone
    return True

# Example usage (for testing purposes)
if __name__ == "__main__":
    # Populate the simulated database
    database[1] = {"name": "Alice", "phone": "+1234567890"}

    # Construct a valid payload
    test_payload = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_phone": "+0987654321"}
    }

    result = change_user_phone(test_payload)
    print("Update successful:", result)   # Should print: Update successful: True
    print("New phone:", database[1]["phone"])  # Should print the updated number