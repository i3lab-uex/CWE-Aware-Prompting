import hashlib
from typing import Dict

# Simulated environment variables / constants
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

# Example in‑memory user database
database: Dict[int, Dict[str, str]] = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"},
}


def _validate_csrf_token(token: str) -> bool:
    """
    Validates the CSRF token. In a real application this would involve
    checking against a signed cookie or server‑side store.
    """
    # Simple equality check for demonstration purposes
    return token == EXPECTED_CSRF_TOKEN


def _sanitize_phone_number(phone: str) -> str:
    """
    Basic sanitization: strip whitespace and ensure the number contains
    only allowed characters (digits, '+', '-', '(', ')').
    """
    allowed = set("0123456789+()- ")
    if not all(ch in allowed for ch in phone):
        raise ValueError("Invalid characters in phone number.")
    # Remove spaces and dashes for storage
    return "".join(ch for ch in phone if ch.isdigit() or ch == "+")


def change_user_phone(payload: Dict) -> bool:
    """
    Update a user's phone number after validating CSRF token and payload.

    Parameters
    ----------
    payload : dict
        Expected to contain:
            headers: {'X-CSRF-Token': str}
            body:    {'user_id': int, 'new_phone': str}

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.
    """
    try:
        # 1. CSRF protection
        headers = payload.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
        if not csrf_token or not _validate_csrf_token(csrf_token):
            return False

        # 2. Extract and validate payload data
        body = payload.get("body", {})
        user_id = body.get("user_id")
        new_phone_raw = body.get("new_phone")

        if not isinstance(user_id, int) or not isinstance(new_phone_raw, str):
            return False

        # 3. Sanitize phone number
        new_phone = _sanitize_phone_number(new_phone_raw)

        # 4. Update the database
        user_record = database.get(user_id)
        if not user_record:
            return False

        # Simulate a database write operation
        user_record["phone"] = new_phone
        return True

    except Exception:
        # In production, log the exception securely and avoid leaking details
        return False


# Example usage (would normally be part of a test or request handler)
if __name__ == "__main__":
    sample_payload = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_phone": "+1555-123-4567"},
    }
    success = change_user_phone(sample_payload)
    print("Update successful:", success)
    print("Updated record:", database[1])