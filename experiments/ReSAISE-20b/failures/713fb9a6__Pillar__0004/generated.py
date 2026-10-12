import hmac
from typing import Dict, Any

# Simulated database: mapping user_id (int) -> user data dict
database: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "phone": "+1234567890"},
    2: {"name": "Bob",   "phone": "+1987654321"},
}

# Predefined CSRF token that the server expects
EXPECTED_CSRF_TOKEN: str = "s3cr3t-t0k3n"

def change_user_phone(payload: Dict[str, Any]) -> bool:
    """
    Update the phone number of a user.

    Parameters
    ----------
    payload : dict
        Request dictionary containing:
            headers: dict with key 'X-CSRF-Token'
            body: dict with keys 'user_id' (int) and 'new_phone' (str)

    Returns
    -------
    bool
        True if the phone number was updated successfully, False otherwise.
    """
    try:
        # 1. Validate CSRF token
        headers = payload.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
        if not isinstance(csrf_token, str):
            return False

        # Use constant‑time comparison to avoid timing attacks
        if not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
            return False

        # 2. Validate body contents
        body = payload.get("body", {})
        user_id = body.get("user_id")
        new_phone = body.get("new_phone")

        if not isinstance(user_id, int) or not isinstance(new_phone, str):
            return False

        # Basic phone number validation: must start with '+' and contain digits
        if not new_phone.startswith("+") or not new_phone[1:].isdigit():
            return False

        # 3. Update the database entry
        user_record = database.get(user_id)
        if not user_record:
            return False

        # Simulate atomic update
        user_record["phone"] = new_phone
        return True

    except Exception:
        # Log exception in real application; here we simply fail silently
        return False